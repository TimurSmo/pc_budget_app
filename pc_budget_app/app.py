from flask import Flask, render_template, request
from suggest_pc_parts import suggest_pc_parts
from pc_parts import pc_parts

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            budget = float(request.form['budget'])
            if budget <= 0:
                raise ValueError

            allocations = {
                'CPU': float(request.form['cpu_allocation']),
                'Motherboard': float(request.form['motherboard_allocation']),
                'GPU': float(request.form['gpu_allocation']),
                'RAM': float(request.form['ram_allocation']),
                'Storage': float(request.form['storage_allocation']),
                'Power Supply': float(request.form['psu_allocation']),
                'Case': float(request.form['case_allocation'])
            }

            if sum(allocations.values()) != 100:
                raise ValueError("Allocations must sum up to 100%.")
        except ValueError as e:
            return render_template('index.html', error=str(e), parts=pc_parts)

        selected_parts, cost, unavailable_parts = suggest_pc_parts(budget, allocations)

        if selected_parts is None:
            return render_template('index.html', error="Not enough budget to buy any parts.", parts=pc_parts)

        if unavailable_parts:
            message = f"Not enough budget to fully assemble the PC. Missing parts: {', '.join(unavailable_parts)}."
        else:
            message = "PC parts selected successfully"

        return render_template('index.html', selected_parts=selected_parts, cost=cost, budget=budget, message=message,
                               parts=pc_parts)

    return render_template('index.html', parts=pc_parts)


if __name__ == '__main__':
    app.run(debug=True)

