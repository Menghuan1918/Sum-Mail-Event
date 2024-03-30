"""
这是一个测试模块是否正常工作的文件
"""

test_txt = """
Subject: Join Us for a Gathering Tonight!

Dear [Recipient's Name],

I hope this message finds you well! I'm reaching out to extend an invitation for you to join us for a casual get-together at my place tonight. It's all about unwinding, enjoying each other's company, and indulging in some tasty food and drinks.

Here are the details:

    Date & Time: Tonight, starting at 7 PM
    Venue: [Your Address], Apartment number [Your Apartment Number]
    Activities: We'll have games, music, and a buffet-style dinner
    Dress Code: Casual, wear whatever makes you feel comfortable

I'll be preparing some snacks and beverages, but feel free to bring along anything you'd like to share!

Please let me know by this afternoon if you can make it. If you have any questions or need further information, don't hesitate to reach out.

Looking forward to seeing you tonight!

Best Wishes,

[Your Name]
"""
from Tools.LLM.Choose import choose

choose_list = ["This is an event notification email and does not require a reply.", "It's a spam email.", "This is an event notification email that requires a reply."]

background = "You are a recipient of the email below and are deciding how to respond."
print(choose(choose_list, test_txt, background))