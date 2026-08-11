import pulp


def solve_security_allocation(
    halls,
    guards,
    required_guards,
    risk_level,
    max_workload
):
    model = pulp.LpProblem(
        "Museum_Security_Guard_Allocation",
        pulp.LpMinimize
    )

    # x[i][j] = تعداد نگهبان j در سالن i
    x = {}

    for i in range(len(halls)):
        for j in range(len(guards)):
            x[i, j] = pulp.LpVariable(
                f"x_{i}_{j}",
                lowBound=0,
                cat="Integer"
            )

    # هدف:
    # کمینه کردن هزینه نیروی انسانی
    model += pulp.lpSum(
        x[i, j] * guards[j]["cost"]
        for i in range(len(halls))
        for j in range(len(guards))
    )

    # هر سالن حداقل تعداد مشخصی نگهبان داشته باشد
    for i, hall in enumerate(halls):
        model += (
            pulp.lpSum(x[i, j] for j in range(len(guards)))
            >= required_guards[i]
        )

    # سالن‌های پرخطر نیروی بیشتری نیاز دارند
    for i, hall in enumerate(halls):
        if risk_level[i] >= 8:
            model += (
                pulp.lpSum(x[i, j] for j in range(len(guards)))
                >= required_guards[i] + 1
            )

    # محدودیت تعداد کل نیرو
    model += pulp.lpSum(
        x[i, j]
        for i in range(len(halls))
        for j in range(len(guards))
    ) <= max_workload

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    result = []

    for i, hall in enumerate(halls):
        row = {
            "hall": hall,
            "guards": []
        }

        for j, guard in enumerate(guards):
            value = int(pulp.value(x[i, j]) or 0)

            if value > 0:
                row["guards"].append({
                    "name": guard["name"],
                    "count": value
                })

        result.append(row)

    return {
        "status": pulp.LpStatus[model.status],
        "objective": pulp.value(model.objective),
        "allocation": result
    }