from pc_parts import pc_parts

def suggest_pc_parts(budget, allocations):
    selected_parts = {}
    total_cost = 0
    cpu_compatibility = None
    motherboard_compatibility = None
    unavailable_parts = []

    for part_type, allocation in allocations.items():
        allocated_budget = budget * (allocation / 100)
        compatible_parts = []

        for part in pc_parts[part_type]:
            if part['price'] <= allocated_budget:
                compatible_parts.append(part)

        if not compatible_parts:
            unavailable_parts.append(part_type)
            continue

        # Select the most expensive part within the budget
        best_part = max(compatible_parts, key=lambda x: x['price'])

        # Check compatibility if it's a CPU or Motherboard
        if part_type == 'Motherboard':
            motherboard_compatibility = best_part['compatibility']
        elif part_type == 'CPU':
            cpu_compatibility = best_part['compatibility']
            if motherboard_compatibility and cpu_compatibility != motherboard_compatibility:
                # If CPU and Motherboard compatibility doesn't match, find another CPU
                compatible_cpus = [part for part in compatible_parts if part['compatibility'] == motherboard_compatibility]
                if not compatible_cpus:
                    unavailable_parts.append(part_type)
                    continue
                best_part = max(compatible_cpus, key=lambda x: x['price'])

        selected_parts[part_type] = best_part
        total_cost += best_part['price']

    if not selected_parts:
        return None, total_cost, "Not enough budget to buy any parts."

    return selected_parts, total_cost, unavailable_parts
