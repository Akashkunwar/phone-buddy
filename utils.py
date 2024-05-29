def generate_prompt(ram, storage, camera, processor, display_size, price, company, battery, prompt):
    parts = ["List of 2 best phones with following minimum specs:"]
    if ram:
        parts.append(f"ram - {', '.join(ram)}")
    if storage:
        parts.append(f"rom - {', '.join(storage)}")
    if battery:
        parts.append(f"rom - {', '.join(battery)}")
    if camera:
        parts.append(f"front camera - {camera[0] if camera else ''}, back camera - {camera[-1] if camera else ''}")
    if display_size:
        parts.append(f"screen size - {', '.join(display_size)}")
    if processor:
        parts.append(f"processor - {', '.join(processor)}")
    if company:
        parts.append(f"company - {', '.join(company)}")
    if price:
        parts.append(f"under price {price[1]} INR")
    prompt_text = ", ".join(parts)
    prompt_text += f" {prompt}. Output results in json with phone name being primary key and specs being nested key: value pair. Make sure to include price in INR"
    return prompt_text