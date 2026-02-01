from responder import Responder


if __name__ == "__main__":

    responder = Responder()

    user_query = "What is (2 + 3) * 10?"
    final_result = 50

    reply = responder.generate_response(user_query, final_result)

    print("\nFINAL RESPONSE:\n")
    print(reply)
