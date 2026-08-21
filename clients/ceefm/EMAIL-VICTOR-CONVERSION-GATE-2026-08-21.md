# Draft email to Victor — conversion action gate
Status: DRAFT, not sent. 2026-08-21.
To: office@ceefm.eu (Victor Danmagaji, Managing Director, CEEFM Kft)
Context: unpaid ad-hoc support. Engagement closed June 2026. Not a reactivation.

---

**Subject:** CEEFM Ads conversion: one question before I change anything

Victor,

Short version. The "conversion action wasn't detected" warning you saw is most likely a false alarm. I need one thing from you to be certain.

That troubleshooter loads the page and watches for the tag. It cannot fill in and submit the contact form. Your conversion fires only on a real submit. So that tool can never detect it, whether it works or not. The warning is expected behaviour, not evidence of a fault.

There is one real question underneath it.

In Google Ads, go to Goals, then Conversions, then Summary. Open the "Contact (Form submission www.ceefm.eu/)" action and tell me two things:

1. Is any conversion action in the account set to the event name `ads_conversion_Contact_Us_2`?
2. What is the "Contact" action matched on: an event name, a conversion label, or Google's automatic form detection?

That decides everything. If an action is bound to that event name, the site is already correct and nothing should change. If nothing is, there is a small change on our side, already written and built, ready to deploy.

I have not touched the live site. I did not want to guess. Applying the change when the current setup is already correct would break a conversion that works today.

Three other things while you are in there.

- `ads_conversion_Contact_Us_1` fires when someone loads /contact/, not when they submit. We did not add it. If it is set as a primary conversion, Google is bidding toward page views instead of enquiries. Worth demoting to secondary or removing. This one is costing you money now.
- Check the Contact action is type Website and not a GA4 import, with Count set to "One". A GA4 import will never match a page-side event, and the symptom looks identical to a broken tag.
- The privacy policy published on the site in August is legal text under CEEFM Kft's name. You have not read it yet. Please do. It also says nothing about remarketing either way, so if the Ads account builds remarketing audiences it needs a sentence adding.

Last thing, unrelated. You gave me Hostinger Collaborator access on 11 August so I could deploy. It covers domain, hosting and email, and it is still active. Please revoke it. The engagement closed in June and there is no reason for me to hold access to your mailbox.

Emmanuel
