"""Read-only openLCA IPC adapter with explicit lifecycle handling."""

from __future__ import annotations

import socket
from typing import Any

from .common import LCAToolError, json_safe, package_version, platform_snapshot, utc_now


def snapshot(*, host: str = "127.0.0.1", port: int = 8080, check_endpoint: bool = False, timeout: float = 1.0) -> dict[str, Any]:
    from importlib.util import find_spec

    modules = {name: find_spec(name) is not None for name in ("olca_ipc", "olca_schema", "olca")}
    current = modules["olca_ipc"] and modules["olca_schema"]
    legacy = modules["olca"]
    generation = (
        "both-current-and-legacy-visible" if current and legacy else
        "current-schema-separated" if current else
        "legacy-monolithic" if legacy else
        "no-python-client-detected"
    )
    endpoint: dict[str, Any] = {
        "host": host,
        "port": port,
        "tcp_checked": check_endpoint,
        "tcp_reachable": None,
        "interpretation": "Transport-only check; database/API/model identity remains manual.",
    }
    if check_endpoint:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                endpoint["tcp_reachable"] = True
        except OSError as exc:
            endpoint["tcp_reachable"] = False
            endpoint["tcp_error"] = f"{type(exc).__name__}: {exc}"
    return {
        "schema_version": "1.0",
        **platform_snapshot(),
        "packages": {
            "olca-ipc": package_version("olca-ipc"),
            "olca-schema": package_version("olca-schema"),
            "olca": package_version("olca"),
        },
        "modules_visible": modules,
        "detected_api_generation": generation,
        "endpoint": endpoint,
        "required_manual_fields": [
            "openlca_application_or_server_version",
            "active_database_name_and_version_or_hash",
            "lcia_package_version",
        ],
    }


def _current_modules() -> tuple[Any, Any]:
    try:
        import olca_ipc as ipc  # type: ignore
        import olca_schema as schema  # type: ignore
    except ImportError as exc:
        raise LCAToolError(
            "Current openLCA Python clients are unavailable. Install compatible olca-ipc and "
            "olca-schema packages, or use the documented legacy workflow in a pinned environment."
        ) from exc
    return ipc, schema


def _client(ipc: Any, host: str, port: int) -> Any:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise LCAToolError("This bundled JSON-RPC adapter only permits a local openLCA endpoint by default.")
    try:
        return ipc.Client(port)
    except TypeError:
        try:
            return ipc.Client(f"http://{host}:{port}")
        except Exception as exc:  # pragma: no cover - depends on installed API generation
            raise LCAToolError(f"Unable to create openLCA client: {exc}") from exc


def list_descriptors(entity_type: str, *, host: str = "127.0.0.1", port: int = 8080, limit: int = 1000) -> dict[str, Any]:
    ipc, schema = _current_modules()
    cls = getattr(schema, entity_type, None)
    if cls is None:
        allowed = [name for name in ("ProductSystem", "ImpactMethod", "Process", "Flow", "Project") if hasattr(schema, name)]
        raise LCAToolError(f"Unknown schema entity type {entity_type!r}; examples: {', '.join(allowed)}")
    client = _client(ipc, host, port)
    try:
        descriptors = list(client.get_descriptors(cls))[:limit]
    except Exception as exc:
        raise LCAToolError(f"openLCA descriptor query failed: {exc}") from exc
    return {
        "generated_utc": utc_now(),
        "entity_type": entity_type,
        "count": len(descriptors),
        "truncated_at": limit,
        "descriptors": [json_safe(item) for item in descriptors],
    }


def calculate(
    product_system_id: str,
    impact_method_id: str | None,
    *,
    amount: float = 1.0,
    host: str = "127.0.0.1",
    port: int = 8080,
    include_inventory: bool = True,
) -> dict[str, Any]:
    if not product_system_id.strip():
        raise LCAToolError("product_system_id is required")
    if amount <= 0:
        raise LCAToolError("amount must be positive")
    ipc, schema = _current_modules()
    ref_type = getattr(schema, "RefType", None)
    if ref_type is None or not hasattr(ref_type, "ProductSystem"):
        raise LCAToolError("Installed olca-schema lacks RefType.ProductSystem; client/schema versions may be incompatible")
    target = schema.Ref(ref_type=ref_type.ProductSystem, id=product_system_id)
    kwargs: dict[str, Any] = {"target": target, "amount": amount}
    if impact_method_id:
        kwargs["impact_method"] = schema.Ref(id=impact_method_id)
    setup = schema.CalculationSetup(**kwargs)
    client = _client(ipc, host, port)
    result = None
    started = utc_now()
    try:
        result = client.calculate(setup)
        if hasattr(result, "wait_until_ready"):
            result.wait_until_ready()
        impacts: list[dict[str, Any]] = []
        if impact_method_id:
            for category in result.get_impact_categories():
                value = result.get_total_impact_value_of(category)
                impacts.append({
                    "category": json_safe(category),
                    "value": json_safe(value),
                })
        inventory = []
        if include_inventory and hasattr(result, "get_total_flows"):
            inventory = [json_safe(item) for item in result.get_total_flows()]
        return {
            "schema_version": "1.0",
            "started_utc": started,
            "completed_utc": utc_now(),
            "adapter": "openlca-current-schema-separated",
            "packages": {
                "olca-ipc": package_version("olca-ipc"),
                "olca-schema": package_version("olca-schema"),
            },
            "endpoint": {"host": host, "port": port},
            "request": {
                "product_system_id": product_system_id,
                "impact_method_id": impact_method_id,
                "amount": amount,
            },
            "impacts": impacts,
            "inventory": inventory,
            "manual_verification_required": [
                "active_database_identity",
                "functional_unit_and_reference_flow",
                "database_system_model",
                "method_implementation_and_flow_mapping",
            ],
        }
    except LCAToolError:
        raise
    except Exception as exc:
        raise LCAToolError(f"openLCA calculation failed: {type(exc).__name__}: {exc}") from exc
    finally:
        if result is not None:
            try:
                if hasattr(result, "dispose"):
                    result.dispose()
                elif hasattr(client, "dispose"):
                    client.dispose(result)
            except Exception:
                pass
