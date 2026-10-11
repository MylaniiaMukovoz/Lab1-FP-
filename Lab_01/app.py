from core import make_processor, Usage

def main():
    usages: list[Usage] = [
        {"id": 1, "minutes": 100, "sms": 20, "traffic_mb": 1024, "tariff": "Basic"},
        {"id": 2, "minutes": 500, "sms": 100, "traffic_mb": 5000, "tariff": "Pro"},
        {"id": 3, "minutes": 10, "sms": 0, "traffic_mb": 100, "tariff": "Basic"}
    ]

    def my_tariff(minutes: int, sms: int, traffic_mb: float) -> float:
        return (minutes * 1.0) + (sms * 0.5) + (traffic_mb * 0.1)

    def my_bonus(cost: float) -> float:
        if cost > 100:
            return cost * 0.9 
        return cost

    processor = make_processor(
        calculate_base_cost=my_tariff,
        apply_bonus=my_bonus
    )

    result = processor(usages)

    print("--- Розшифровка мобільного тарифу за місяць ---")
    for record in result["records"]:
        print(f"Абонент #{record['id']} | Тариф: {record['tariff']} | До оплати: {record['monthly_cost']:.2f} грн")
    
    print("-" * 45)
    print(f"Оброблено абонентів: {result['count']}")
    print(f"Загальний дохід компанії: {result['revenue']:.2f} грн")

if __name__ == "__main__":
    main()