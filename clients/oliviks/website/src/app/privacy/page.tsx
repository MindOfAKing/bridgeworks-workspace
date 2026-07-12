import type { Metadata } from 'next';
import { site } from '@/data/site';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'How Oliviks Kitchen collects, uses, and protects your personal data under GDPR.',
};

// Foundation A3 deliverable #6 — GDPR privacy policy.
// DRAFT: Aese/Cynthia to confirm the legal entity name and any data processors
// before this is treated as final. Written for the data actually collected here:
// the contact form, the specials sign-up list, and the WooCommerce shop.

const updated = 'July 2026';

export default function PrivacyPage() {
  return (
    <div className="container-x max-w-3xl py-16 sm:py-20">
      <p className="eyebrow">
        <span className="eyebrow-num">·</span> Legal
      </p>
      <h1 className="mt-4 font-display text-[clamp(2.2rem,5vw,3.2rem)] font-extrabold tracking-tight text-cocoa">
        Privacy Policy
      </h1>
      <p className="mt-3 text-[14px] text-cocoa/55">Last updated: {updated}</p>

      <div className="mt-8 space-y-7 text-[15.5px] leading-relaxed text-cocoa/75 [&_h2]:font-display [&_h2]:text-[20px] [&_h2]:font-extrabold [&_h2]:text-cocoa [&_a]:font-semibold [&_a]:text-palm [&_a]:underline">
        <p>
          This policy explains what personal data Oliviks Kitchen collects through this website,
          why we collect it, and the rights you have under the EU General Data Protection Regulation
          (GDPR) and Hungarian data protection law.
        </p>

        <section className="space-y-2">
          <h2>Who we are</h2>
          <p>
            Oliviks Kitchen, Rákóczi tér 9, 1084 Budapest, Hungary. For any privacy question or
            request, contact us at{' '}
            <a href={`mailto:${site.email}`}>{site.email}</a> or {site.phone.display}.
          </p>
        </section>

        <section className="space-y-2">
          <h2>What we collect and why</h2>
          <ul className="list-disc space-y-2 pl-5">
            <li>
              <strong>Specials sign-up.</strong> If you join our list, we store the email address
              and, optionally, the WhatsApp number you give us, so we can send you menu specials and
              offers. We only do this after you tick the consent box. Legal basis: your consent.
            </li>
            <li>
              <strong>Contact and catering enquiries.</strong> When you send a message, we receive
              your name, email, and what you wrote, so we can reply. Legal basis: taking steps at
              your request.
            </li>
            <li>
              <strong>Orders.</strong> Orders placed through our online shop are handled on
              shop.oliviks.com and are used to prepare and fulfil your order. Legal basis:
              performance of your order.
            </li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2>How long we keep it</h2>
          <p>
            We keep sign-up data until you unsubscribe or ask us to delete it. Every marketing email
            includes an unsubscribe link, and you can reply STOP to any WhatsApp message to opt out.
            Enquiry messages are kept only as long as needed to handle your request.
          </p>
        </section>

        <section className="space-y-2">
          <h2>Who we share it with</h2>
          <p>
            We do not sell your data. We use trusted service providers to run the website and send
            messages on our behalf (for example, our email delivery provider and our website host).
            They process data only on our instructions.
          </p>
        </section>

        <section className="space-y-2">
          <h2>Your rights</h2>
          <p>
            You can ask us to access, correct, or delete your data, or to stop using it, at any time.
            Email <a href={`mailto:${site.email}`}>{site.email}</a>. You also have the right to
            complain to the Hungarian National Authority for Data Protection and Freedom of
            Information (NAIH).
          </p>
        </section>
      </div>
    </div>
  );
}
