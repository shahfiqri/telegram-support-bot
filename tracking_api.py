import requests

def track(tracking_number):
    """Semak status penghantaran melalui API tracking.my."""
    url = f"https://api.tracking.my/v3/track/{tracking_number}"
    headers = {"Authorization": "Js8Z8BoVXkzO4mBjDYHTcsRdoUC2pe76"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("latest_status", "Tiada maklumat terkini.")
    else:
        return "Gagal mendapatkan maklumat tracking."
