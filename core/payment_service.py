import razorpay
from django.conf import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


def create_order(amount):

    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return order
def verify_payment(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):

    client.utility.verify_payment_signature({
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature
    })

    return True
def capture_payment(
    razorpay_payment_id,
    amount
):

    payment = client.payment.capture(
        razorpay_payment_id,
        amount * 100
    )

    return payment