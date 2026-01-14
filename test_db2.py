from send_to_db import send_detection_to_db

ok = send_detection_to_db(
    material="plastic",
    description="Detected material: plastic",
    image_url="http://127.0.0.1:8000/output/frames/teste.jpg",
    latitude=38.7,
    longitude=-9.2,
    stick_id=1
)

print("DB OK?", ok)
