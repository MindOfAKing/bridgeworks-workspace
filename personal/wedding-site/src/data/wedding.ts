// Single source of truth for every word and date on the wedding site.
// Edit this file only. Nothing else needs touching to fill the site in.
//
// Anything still starting with "TODO:" is a placeholder. Placeholders are
// visible on the page so nothing invented is ever shown to a guest by accident.

import { sampleWedding } from './wedding.sample';

export const PLACEHOLDER = 'TODO:';

// Preview mode swaps in invented sample content so the design can be judged
// with real length copy. It is opt in through the environment, never the
// default, and the page carries a ribbon whenever it is on.
export const isSampleContent = process.env.NEXT_PUBLIC_PREVIEW_SAMPLE === '1';

export function isPlaceholder(value: string | undefined | null): boolean {
  return typeof value === 'string' && value.trimStart().startsWith(PLACEHOLDER);
}

export type EventBlock = {
  label: string;
  time: string;
  venue: string;
  address: string;
  mapsUrl: string;
  note: string;
};

export type StoryEntry = {
  when: string;
  title: string;
  body: string;
};

export type PlanEntry = {
  title: string;
  body: string;
};

export type Photo = {
  src: string;
  alt: string;
  caption: string;
};

export type Wedding = {
  couple: { one: string; two: string; shortLabel: string };
  date: { display: string; iso: string };
  city: string;
  invitationLine: string;
  dressCode: string;
  ceremony: EventBlock;
  reception: EventBlock;
  rsvp: {
    deadlineIso: string;
    deadlineDisplay: string;
    intro: string;
    thanks: string;
    thanksDecline: string;
  };
  gifts: { heading: string; body: string[] };
  loveStory: { heading: string; entries: StoryEntry[] };
  afterPlans: { heading: string; intro: string; entries: PlanEntry[] };
  gallery: { heading: string; photos: Photo[] };
  contactEmail: string;
};

const realWedding: Wedding = {
  // Names as they should read on the invitation.
  couple: {
    one: 'Emmanuel',
    two: 'Flóra',
    // Shown in the browser tab and on the unlock screen.
    shortLabel: 'Emmanuel & Flóra',
  },

  // Human readable date and the machine date used for countdowns and sorting.
  // The month is confirmed, the day is not. Set both once the date is fixed.
  date: {
    display: 'TODO: Saturday, 00 October 2026',
    iso: '2026-10-01',
  },

  city: 'Budapest, Hungary',

  // A line or two under the names on the invitation.
  invitationLine: 'TODO: together with their families, invite you to celebrate their wedding',

  dressCode: 'TODO: dress code, or delete this line',

  ceremony: {
    label: 'Ceremony',
    time: 'TODO: 00:00',
    venue: 'TODO: venue name',
    address: 'TODO: street, postal code, city',
    mapsUrl: '',
    note: 'TODO: anything guests should know, such as arrival time or parking',
  },

  reception: {
    label: 'Reception',
    time: 'TODO: 00:00',
    venue: 'TODO: venue name',
    address: 'TODO: street, postal code, city',
    mapsUrl: '',
    note: 'TODO: anything guests should know, such as travel between venues',
  },

  rsvp: {
    // Guests can submit up to and including this date. After it the form closes.
    deadlineIso: '2026-09-30',
    deadlineDisplay: '30 September 2026',
    intro: 'TODO: a warm line asking guests to reply by the date above',
    // Shown after a successful submission.
    thanks: 'Thank you. Your reply is in, and we cannot wait to see you.',
    // Shown after a successful submission from someone who cannot come.
    thanksDecline: 'Thank you for letting us know. You will be missed.',
  },

  gifts: {
    heading: 'Gifts',
    // Replace with the wording adapted from the Movi and Dani e-vite.
    body: [
      'TODO: paragraph one. Your presence is the gift, and nothing more is expected.',
      'TODO: paragraph two. If you would like to give something, a contribution towards the life we are building together means the most to us.',
    ],
  },

  loveStory: {
    heading: 'Our story',
    entries: [
      { when: 'TODO: year', title: 'TODO: how we met', body: 'TODO: two or three sentences.' },
      { when: 'TODO: year', title: 'TODO: a moment that mattered', body: 'TODO: two or three sentences.' },
      { when: 'TODO: year', title: 'TODO: the proposal', body: 'TODO: two or three sentences.' },
    ],
  },

  afterPlans: {
    heading: 'After the ceremony and reception',
    intro: 'TODO: one line setting up what happens once the formal part ends.',
    entries: [
      { title: 'TODO: after the ceremony', body: 'TODO: where guests go, how long the gap is, what to expect.' },
      { title: 'TODO: after the reception', body: 'TODO: the afterparty, the venue, the finish time.' },
      { title: 'TODO: the next day', body: 'TODO: anything happening the morning after, or delete this entry.' },
    ],
  },

  gallery: {
    heading: 'Us',
    // Drop image files into public/photos/ and point src at them, for example
    // '/photos/engagement-01.jpg'. Alt text is required on every photo.
    photos: [],
  },

  // Reply address shown to guests if they would rather write than use the form.
  // Leave empty to hide the line entirely.
  contactEmail: '',
};

export const wedding: Wedding = isSampleContent ? sampleWedding : realWedding;
