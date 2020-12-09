'''
Getting rec(s) from the db and format it to json
To send back to user request
'''
def appt_obj(appt):

    return_obj = {
        "id":             appt.external_id,
        "first_name":     appt.first_name,
        "last_name":      appt.last_name,
        "service":        appt.service,
        "status":         appt.status,
        "street_address": appt.street_address,
        "city":           appt.city,
        "state":          appt.state,
        "zip":            appt.zip,
        "phone":          appt.phone,
        "date":           str(appt.date.isoformat()[:19]) +"Z",
        "price":          str(appt.price),
        "links": [
            { "rel": "self", "href": "/appts/" + appt.external_id },
      ]
    }

    return return_obj

# when have more than one record
def appts_obj(appts):

    appts_obj_list = []
    for appt in appts.items:
        appts_obj_list.append(appt_obj(appt))

    return appts_obj_list
