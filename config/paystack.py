from paystackapi.paystack import Paystack
paystack_secret_key = "sk_test_9640b418804fec8f77c42721b638d18fde43bf4a" 
paystack = Paystack(secret_key=paystack_secret_key)

# to use transaction class
paystack.transaction.list()

# # to use customer class
# paystack.customer.get(transaction_id)

# # to use plan class
# paystack.plan.get(plan_id)

# # to use subscription class
# paystack.subscription.list()