from service.gmail_service import GmailService


def main():
    """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
    gmail_service = GmailService()

    spam_label_id = gmail_service.get_label_id("SPAM")
    gmail_service.get_messages_by_label(spam_label_id, 10)


if __name__ == "__main__":
    main()
