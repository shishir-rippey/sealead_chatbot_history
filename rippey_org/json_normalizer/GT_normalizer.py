import json




with open("model_bol.json", "r") as json_file:
    json_data = json.load(json_file)

key_list = [
    "_id", "shipper", "name", "address",
    "consignee", "notify", "stuffing_location", "consolidator", "seller",
    "buyer", "manufacturer", "ship_to", "importer", "bill_to", "customer",
    "vendor", "port_of_discharge", "port_of_discharge_code",
    "port_of_loading", "port_of_loading_code", "place_of_delivery",
    "place_of_delivery_code", "place_of_receipt", "final_destination",
    "port_of_export", "departure", "pickup_location_name",
    "pickup_location_address", "delivery_location_address", "agent_iata_code",
    "airport_of_departure", "airport_of_departure_code", "origin_airport_code",
    "cargo_pickup_location_address", "cargo_pickup_location_name",
    "airport_of_destination", "airport_of_destination_code", "arrival_port_code",
    "vessel_name", "voyage_number",  "file_type",
    "bill_of_lading", "shipping_comp", "scac_code", "reference",
    "marks_and_numbers", "shipped_on_board_date", "onboard_vessel", "onboard_date",
    "freight_amount", "number_of_originals", "num_of_copy", "release_type",
    "bill_of_lading_requirement", "invoice_date", "carrier_code",
    "etd", "eta", "payment_terms", "total_quantity",
    "total_weight", "total_weight_uom", "print_date", "container_gross_weight",
    "invoice_currency", "invoice_date", "invoice_entity", "payment_method",
    "temperature", "pickup_date", "total_amount", "commodity", "commodity_code",
    "service_no", "measurement", "measurement_uom", "date_of_issue",
    "place_of_issue", "container_number", "container_size",
    "hs_code", "container_type", "seal_number", "load_type", "weight",
    "weight_uom", "part_number", "volume", "volume_uom", "move_type",
    "chargeable_weight", "item_number", "description", "gross_weight",
    "gross_weight_uom", "bl_quantity", "bl_quantity_uom",
    "quantity", "quantity_uom", "error", "message"
]



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
        del normalized_data["entity_code"]
    final_json.append(normalized_data)

    with open("normalized_data.json", "w") as output_file:
        json.dump(final_json, output_file, indent=4)

    print("Normalized data saved successfully to normalized_data.json")
