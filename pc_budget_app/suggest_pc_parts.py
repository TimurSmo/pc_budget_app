from pc_parts import pc_parts

def suggest_pc_parts(budget, allocations):
    selected_parts = {}
    total_cost = 0
    unavailable_parts = []

    # Compatibility dictionary to track the required compatibility
    compatibility = {}

    for part_type, allocation in allocations.items():
        allocated_budget = budget * (allocation / 100)
        compatible_parts = []

        for part in pc_parts[part_type]:
            # Check compatibility for CPU and Motherboard
            if part_type == 'CPU':
                if 'Motherboard' in selected_parts and selected_parts['Motherboard']['compatibility'] != part['compatibility']:
                    continue
                compatibility['CPU'] = part['compatibility']

            if part_type == 'Motherboard':
                if 'CPU' in selected_parts and selected_parts['CPU']['compatibility'] != part['compatibility']:
                    continue
                compatibility['Motherboard'] = part['compatibility']

            if part['price'] <= allocated_budget:
                compatible_parts.append(part)

        if not compatible_parts:
            unavailable_parts.append(part_type)
            continue

        best_part = max(compatible_parts, key=lambda x: x['price'])

        selected_parts[part_type] = best_part
        total_cost += best_part['price']

    if not selected_parts:
        return None, total_cost, "Not enough budget to buy any parts"

    return selected_parts, total_cost, unavailable_parts