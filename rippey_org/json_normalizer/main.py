import json




with open("model_bol.json", "r") as json_file:
    json_data = json.load(json_file)

key_list = ["filename", "_id", "entity_code", "bl_quantity", "bl_quantity_uom", "load_type", "container_no", "seal_no",
            "container_type", "container_size", "weight", "volume", "move_type", "hs_code", "error", "message",
            "bol_type", "hbl_no", "carrier_name", "carrier_code", "shipper", "shipper_name", "shipper_address", "consignee",
            "consignee_name", "consignee_address", "notify_party", "notify_name", "notify_address", "booking_number", "release_type", "etd", "description",
            "port_of_loading", "port_of_loading_code", "port_of_discharge", "port_of_discharge_code", "shipped_on_board_date", "vessel_name", "voyage_number", 
            "payment_method", "gross_weight", "measurement","doc_mode", "doc_type", "doc_status", "load_type", "load_origin", "load_destination", "move_type", "export_carrier"]


def transform_entity_code(entity_code):
    entity_detail = {}
    for entity in entity_code:
        entity_type = entity.get("type")
        if entity_type:
            entity_detail[entity_type] = {k: v for k, v in entity.items() if k != "type"}
    return entity_detail

final_json = []

def nor_json(key_list, data):
    normalized_json = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key in key_list:
                if key in normalized_json:
                    if isinstance(normalized_json[key], list):
                        normalized_json[key].append(value)
                    else:
                        normalized_json[key] = [normalized_json[key], value]
                else:
                    normalized_json[key] = value
            elif isinstance(value, dict):
                nested_json = nor_json(key_list, value)
                for k, v in nested_json.items():
                    if k in normalized_json:
                        if isinstance(normalized_json[k], list):
                            normalized_json[k].append(v)
                        else:
                            normalized_json[k] = [normalized_json[k], v]
                    else:
                        normalized_json[k] = v
            elif isinstance(value, list):
                for item in value:
                    nested_json = nor_json(key_list, item)
                    for k, v in nested_json.items():
                        if k in normalized_json:
                            if isinstance(normalized_json[k], list):
                                normalized_json[k].append(v)
                            else:
                                normalized_json[k] = [normalized_json[k], v]
                        else:
                            normalized_json[k] = v
    elif isinstance(data, list):
        for item in data:
            nested_json = nor_json(key_list, item)
            for k, v in nested_json.items():
                if k in normalized_json:
                    if isinstance(normalized_json[k], list):
                        normalized_json[k].append(v)
                    else:
                        normalized_json[k] = [normalized_json[k], v]
                else:
                    normalized_json[k] = v
    return normalized_json

if __name__ == "__main__":

    # for data in json_data:
    normalized_data = nor_json(key_list=key_list, data=json_data)
    if "entity_code" in normalized_data:
        normalized_data["entity_detail"] = transform_entity_code(normalized_data["entity_code"])
        del normalized_data["entity_code"]  # Remove the old entity_code key if no longer needed
    final_json.append(normalized_data)

    with open("normalized_data.json", "w") as output_file:
        json.dump(final_json, output_file, indent=4)

    print("Normalized data saved successfully to normalized_data.json")
