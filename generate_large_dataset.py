import json
from pathlib import Path


def _pick_labels(config, ticket_number, tenant_id):
    labels = list(config["labels"])
    seed = (ticket_number * 17 + len(tenant_id) * 13) % len(labels)
    primary = labels[seed]
    extras = [label for label in labels if label != primary]
    extra_count = 1 if ticket_number % 3 == 0 else 2 if ticket_number % 5 == 0 else 0
    if extra_count:
        selected = [primary]
        for idx in range(extra_count):
            pick = extras[(seed + idx + ticket_number) % len(extras)]
            if pick not in selected:
                selected.append(pick)
        return selected
    return [primary]


def _render_mixed_text(tenant_id, labels, language, ticket_number, order=None, serial=None):
    text_variants = {
        "acme_corp": {
            "billing|shipping": [
                f"I was double charged on order #{order} and the package still has not moved from the warehouse; I need both the refund and a delivery update.",
                f"My invoice for #{order} is wrong and my shipment tracking shows no movement, so I need this corrected before the next billing cycle.",
            ],
            "billing|account_access": [
                f"I cannot log in to my account after payment failed on order #{order}, and I also need the duplicate charge removed from my card.",
                f"The billing system shows a charge on #{order} but my account is locked, and I need both access restored and the duplicate payment fixed.",
            ],
            "shipping|technical_issue": [
                f"The tracking for #{order} has stalled and the mobile app crashes when I try to view the shipment details from my phone.",
                f"My package for #{order} has not updated in days, and the dashboard errors out whenever I check the order status after login.",
            ],
            "technical_issue|churn_risk": [
                "The app keeps crashing during exports and this repeated failure makes me seriously consider leaving the service unless it is fixed quickly.",
                "The dashboard fails every time I try to run a report, and I am already considering a cancellation because the product is not reliable.",
            ],
            "account_access|feature_request": [
                "I am locked out of my account and also need a better bulk export option so my team can download reports without manual steps.",
                "My login reset email never arrives, and I would also like a simpler CSV export workflow for the whole team.",
            ],
            "billing|feature_request": [
                f"The bill for #{order} is incorrect and I need a cleaner export of invoice records so I can reconcile the charges myself.",
                f"I need the duplicate charge on #{order} reviewed and a bulk export feature so my finance team can pull the report without workarounds.",
            ],
        },
        "globex_manufacturing": {
            "parts_order|technical_issue": [
                f"We need a replacement motor for serial {serial} and the control panel keeps failing in the middle of production, which is causing downtime.",
                f"The line is down because the drive assembly on {serial} failed, and we need the part shipped immediately while the fault is diagnosed.",
            ],
            "warranty_claim|compliance_question": [
                f"We are filing a warranty claim for {serial} and need the compliance statement for the audit before the regulator visit next week.",
                f"The warranty review for {serial} is blocked because we still need the CE documentation and the safety certification packet.",
            ],
            "installation_support|technical_issue": [
                f"We are installing the new unit {serial} and the intake clearance is unclear; the machine also reports an overheating fault during startup.",
                f"We need installation guidance for {serial}, and the operator is seeing repeated overheating warnings during the first production cycle.",
            ],
            "compliance_question|parts_order": [
                f"We need the conformity paperwork for {serial} and also the replacement intake fan part before the audit and line restart.",
                f"The audit is approaching and we still need the CE package for {serial}; we also need the spare gearbox part to resume production.",
            ],
            "warranty_claim|technical_issue": [
                f"The unit {serial} failed within the warranty period and is still producing an overheating warning, so we need a quick claim and diagnosis.",
                f"We are requesting warranty coverage for {serial}, and the machine is throwing the same overheating fault even after the last maintenance visit.",
            ],
        },
    }

    key = "|".join(sorted(labels))
    variants = text_variants.get(tenant_id, {}).get(key, [])
    if variants:
        base = variants[(ticket_number * 7) % len(variants)]
    else:
        base = "Customer issue requires support review."

    if language == "es":
        if tenant_id == "acme_corp":
            if "billing" in labels and "shipping" in labels:
                return f"Necesito ayuda porque me cobraron dos veces en #{order} y mi paquete todavía no se mueve; necesito una factura correcta y una actualización del envío."
            if "billing" in labels and "account_access" in labels:
                return f"No puedo entrar a mi cuenta porque la renovación falló en #{order} y además necesito que eliminen el cobro duplicado de mi tarjeta."
            if "shipping" in labels and "technical_issue" in labels:
                return f"La app falla cuando reviso el pedido #{order}, y el seguimiento sigue detenido sin ninguna actualización del envío."
            if "technical_issue" in labels and "churn_risk" in labels:
                return "La aplicación falla al exportar informes y esto ya me hace pensar en cancelar el servicio si no se corrige rápido."
            if "account_access" in labels and "feature_request" in labels:
                return "Estoy bloqueado y también necesito exportar reportes grandes en CSV sin hacerlo manualmente cada semana."
        else:
            if "parts_order" in labels and "technical_issue" in labels:
                return f"Necesitamos una pieza de repuesto para {serial} y la máquina sigue fallando durante la producción; esto está causando paros."
            if "warranty_claim" in labels and "compliance_question" in labels:
                return f"Necesitamos tramitar la garantía de {serial} y también la documentación de conformidad para la auditoría del próximo lunes."
    if language == "de":
        if tenant_id == "globex_manufacturing":
            if "parts_order" in labels and "technical_issue" in labels:
                return f"Wir brauchen ein Ersatzteil für {serial}, und die Anlage zeigt zudem während der Produktion weiterhin einen Fehler an."
            if "installation_support" in labels and "technical_issue" in labels:
                return f"Wir installieren die Anlage {serial} und benötigen die richtige Einbaubreite; zudem meldet die Maschine beim Start einen Überhitzungsfehler."
            if "warranty_claim" in labels and "compliance_question" in labels:
                return f"Wir prüfen den Garantieanspruch für {serial} und benötigen zugleich die CE-Dokumentation für den nächsten Audit."
    if language == "fr":
        if tenant_id == "globex_manufacturing":
            if "parts_order" in labels and "technical_issue" in labels:
                return f"Nous avons besoin de pièces de rechange pour {serial}, et l'unité affiche toujours une erreur technique pendant la production."
            if "warranty_claim" in labels and "technical_issue" in labels:
                return f"Le matériel {serial} a échoué dans la période de garantie et continue d'afficher une surchauffe; nous demandons un suivi rapide."
            if "compliance_question" in labels and "parts_order" in labels:
                return f"Nous avons besoin de la documentation de conformité pour {serial} ainsi que des pièces de rechange avant le prochain audit."

    return base


def _build_ticket_text(tenant_id, labels, language, ticket_number, order=None, serial=None):
    if len(labels) > 1:
        return _render_mixed_text(tenant_id, labels, language, ticket_number, order=order, serial=serial)

    label = labels[0]
    config = TENANTS[tenant_id]
    templates = config["issue_templates"][label]
    template = templates[(ticket_number * 13 + len(label)) % len(templates)]
    text = template
    if "{order}" in text and order:
        text = text.format(order=order)
    if "{tracking}" in text:
        text = text.format(tracking=f"TRK-{1000 + ticket_number}")
    if "{serial}" in text and serial:
        text = text.format(serial=serial)

    if language == "es":
        if tenant_id == "acme_corp":
            if label == "billing":
                text = f"Necesito ayuda con la factura de #{order}; veo dos cargos iguales y quiero que lo revisen."
            elif label == "shipping":
                text = f"Mi envío #{order} no ha tenido movimiento y necesito saber dónde está el paquete urgente."
            elif label == "technical_issue":
                text = "La aplicación falla al exportar informes desde el móvil y necesito una solución inmediata."
            elif label == "account_access":
                text = "Estoy bloqueado en mi cuenta y necesito acceso de inmediato para seguir trabajando."
            elif label == "churn_risk":
                text = "Estoy considerando cancelar por la repetición del problema y por la falta de estabilidad del servicio."
            elif label == "feature_request":
                text = "Me gustaría tener exportaciones CSV masivas sin hacerlo manualmente cada semana."
        else:
            if label == "technical_issue":
                text = f"La máquina {serial} muestra un fallo de sobrecalentamiento y la línea se ha detenido."
            elif label == "warranty_claim":
                text = f"Solicitamos la garantía para {serial} porque la unidad falló dentro del periodo de cobertura."
            elif label == "parts_order":
                text = f"Necesitamos piezas de reemplazo para {serial} antes de reanudar la producción."
            elif label == "installation_support":
                text = f"Necesitamos orientación para instalar {serial} y confirmar el espacio de ventilación requerido."
            elif label == "compliance_question":
                text = f"Necesitamos la documentación de conformidad de {serial} para la auditoría de esta semana."
    elif language == "de":
        if tenant_id == "globex_manufacturing":
            if label == "technical_issue":
                text = f"Die Anlage {serial} meldet einen Überhitzungsfehler und die Produktion steht still."
            elif label == "warranty_claim":
                text = f"Wir beantragen den Garantieanspruch für {serial}, weil die Maschine innerhalb der Gewährleistung ausfällt."
            elif label == "parts_order":
                text = f"Wir benötigen Ersatzteile für {serial}, bevor die Produktion wieder anlaufen kann."
            elif label == "installation_support":
                text = f"Wir brauchen die Installationsabstände für {serial} und die nötige Anordnung der Anlage."
            elif label == "compliance_question":
                text = f"Wir brauchen die CE-Konformitätserklärung für {serial} für den Prüfungsprozess."
    elif language == "fr":
        if tenant_id == "globex_manufacturing":
            if label == "technical_issue":
                text = f"L'unité {serial} affiche une surchauffe et la production est interrompue."
            elif label == "warranty_claim":
                text = f"Nous déposons une demande de garantie pour {serial} car la machine a échoué dans la période couverte."
            elif label == "parts_order":
                text = f"Nous avons besoin de pièces de rechange pour {serial} avant la reprise de la ligne."
            elif label == "installation_support":
                text = f"Nous avons besoin de la configuration d'installation requise pour {serial} et des distances de sécurité."
            elif label == "compliance_question":
                text = f"Nous avons besoin de la documentation de conformité pour {serial} avant l'audit de cette semaine."

    return text


TENANTS = {
    "acme_corp": {
        "labels": [
            "billing",
            "shipping",
            "technical_issue",
            "account_access",
            "churn_risk",
            "feature_request",
        ],
        "languages": ["en", "es"],
        "orders": ["A5521", "A9981", "A3342", "A7749", "A1189", "A6034"],
        "user_names": ["Sarah", "Mateo", "Priya", "Daniel", "Nadia", "Luis", "Ava", "Olivia"],
        "issue_templates": {
            "billing": [
                "I was charged twice for order #{order} and the payment still looks wrong.",
                "I need a refund for my damaged item from order #{order}, and the charge is higher than expected.",
                "I keep seeing duplicate charges on my card for #{order} and I want this fixed.",
                "The invoice for #{order} is incorrect and I would like the billing team to review it.",
            ],
            "shipping": [
                "My package for order #{order} has not moved in six days and I need a status update.",
                "Tracking number {tracking} has not updated since dispatch and I need delivery information.",
                "The parcel for #{order} was supposed to arrive last week and it still hasn't moved.",
                "I need to know where my shipment for #{order} is; the tracking says it is stuck.",
            ],
            "technical_issue": [
                "The app crashes every time I export my monthly report on iPhone and I need a fix.",
                "I keep getting an error when I open the dashboard after the latest update.",
                "The mobile app freezes during login and makes the workflow unusable.",
                "The website is failing on checkout and I cannot complete my purchase.",
            ],
            "account_access": [
                "My account was locked after too many login attempts and I need access restored.",
                "I cannot sign in because the password reset email never arrives.",
                "I am locked out of my account and this has happened twice this week.",
                "Login keeps failing even after resetting my password and I need support.",
            ],
            "churn_risk": [
                "I am thinking about cancelling because the current pricing is too high.",
                "This keeps happening and I am seriously considering leaving the service.",
                "I may cancel if this is not resolved quickly because I am not satisfied.",
                "I am done with the product unless the issue is corrected immediately.",
            ],
            "feature_request": [
                "Could you add bulk CSV export for all customer records in one click?",
                "It would be useful to have scheduled reports and a cleaner export option.",
                "I need a feature that allows easier offline exports for my team each week.",
                "Please add a simpler way to export large reports in a more efficient format.",
            ],
        },
        "urgency": {
            "billing": ["medium", "high"],
            "shipping": ["high", "medium"],
            "technical_issue": ["medium", "high"],
            "account_access": ["high", "critical"],
            "churn_risk": ["medium", "high"],
            "feature_request": ["low", "medium"],
        },
        "tool_map": {
            "billing": ["order_status", "refund_lookup", "kb_search"],
            "shipping": ["order_status", "kb_search"],
            "technical_issue": ["kb_search"],
            "account_access": ["kb_search"],
            "churn_risk": ["kb_search"],
            "feature_request": [],
        },
    },
    "globex_manufacturing": {
        "labels": [
            "warranty_claim",
            "parts_order",
            "technical_issue",
            "installation_support",
            "compliance_question",
        ],
        "languages": ["en", "de", "fr"],
        "serials": ["GX4000-77812", "GX-4100", "GX-4000", "GX9800-1129", "GX-2200"],
        "issue_templates": {
            "technical_issue": [
                "Our GX-4100 unit is throwing an overheating fault every afternoon and the line is down.",
                "The drive motor on our GX-4000 failed after 14 months and our production output is affected.",
                "The control panel on the machine keeps shutting down during operation and we need support immediately.",
                "The unit is reporting a fault during peak production and we need a fast diagnosis.",
            ],
            "warranty_claim": [
                "We need to file a warranty claim for our GX-4000 after repeated failures in the last year.",
                "The motor assembly failed within the warranty period and we need documentation for the claim.",
                "Our equipment was serviced last quarter and now the warranty claim needs review.",
                "We need warranty coverage for the failed drive unit under our maintenance agreement.",
            ],
            "parts_order": [
                "We need replacement parts for the drive motor and delivery is time critical.",
                "Please help us order the spare drive assembly for our production line before shutdown extends.",
                "We need a replacement intake fan and the line is down while we wait for the part.",
                "The gearbox component failed and we need the exact replacement part as soon as possible.",
            ],
            "installation_support": [
                "We are planning a new GX-4000 installation and need the intake-side clearance requirement.",
                "Can you confirm the installation spacing for the GX-4100 before we begin setup?",
                "We need support on the machine layout and the required clearance around the intake side.",
                "We are installing the new series and want to confirm the mounting clearances in advance.",
            ],
            "compliance_question": [
                "We need the CE compliance declaration for serial number {serial} for next week's audit.",
                "Can you share the certification package for the GX-4000 line before our review meeting?",
                "We need the latest conformity documentation to satisfy the regulator audit schedule.",
                "Please send the compliance and safety paperwork connected to the GX-4100 unit.",
            ],
        },
        "urgency": {
            "technical_issue": ["critical", "high"],
            "warranty_claim": ["high", "medium"],
            "parts_order": ["critical", "high"],
            "installation_support": ["low", "medium"],
            "compliance_question": ["high", "medium"],
        },
        "tool_map": {
            "technical_issue": ["kb_search"],
            "warranty_claim": ["account_lookup", "kb_search"],
            "parts_order": ["account_lookup", "kb_search"],
            "installation_support": ["kb_search"],
            "compliance_question": ["kb_search"],
        },
    },
}


def build_dataset(count: int = 2000, output_path: str = "data/large_tickets.jsonl") -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    ticket_number = 1

    for tenant_id, config in TENANTS.items():
        target = count // len(TENANTS)
        for _ in range(target):
            language = config["languages"][(ticket_number * 3) % len(config["languages"])]
            order = config.get("orders", [])[ticket_number % len(config.get("orders", ["A0001"]))] if "orders" in config else None
            serial = config.get("serials", [])[ticket_number % len(config.get("serials", ["GX0000"]))] if "serials" in config else None
            labels = _pick_labels(config, ticket_number, tenant_id)
            text = _build_ticket_text(tenant_id, labels, language, ticket_number, order=order, serial=serial)
            primary_label = labels[0]
            urgency_rank = config["urgency"].get(primary_label, ["medium"])
            urgency = urgency_rank[(ticket_number * 5) % len(urgency_rank)]
            tool_trace = []
            for label in labels:
                for tool in config["tool_map"].get(label, []):
                    if tool not in tool_trace:
                        tool_trace.append(tool)

            if len(labels) > 1 and ticket_number % 7 == 0:
                text = text + " " + _build_ticket_text(tenant_id, [primary_label], language, ticket_number + 1, order=order, serial=serial)

            rows.append({
                "ticket_id": f"{tenant_id.upper()}-{ticket_number:05d}",
                "tenant_id": tenant_id,
                "language": language,
                "text": text,
                "gold_labels": labels,
                "gold_urgency": urgency,
                "gold_tool_trace": tool_trace,
            })
            ticket_number += 1

    with open(output, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")

    print(f"Generated {len(rows)} tickets at {output}")


if __name__ == "__main__":
    build_dataset(4000)
