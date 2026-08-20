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
    one: 'Flóra',
    two: 'Emmanuel',
    // Shown in the browser tab and on the unlock screen.
    shortLabel: 'Flóra & Emmanuel',
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
      {
        when: '2 May 2025',
        title: 'A concert',
        body: 'We met at a concert. Neither of us went looking for anything, and we left knowing we would see each other again.',
      },
      {
        when: '20 August 2025',
        title: 'We made it official',
        body: 'Three months of hanging out and getting to know each other, properly, without rushing it. Then we stopped calling it anything else.',
      },
      {
        when: 'February 2026',
        title: 'A Sunday afternoon',
        body: 'We came back from church after a Valentine\'s Day service, looked at each other, and said it out loud: I would like to marry you. That has been our pursuit ever since.',
      },
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
    // Real photographs, served straight from public/ behind the gate.
    // Alt text is required on every one of them.
    photos: [
      { src: '/photos/01-vienna-belvedere.jpg', alt: 'Emmanuel kissing Flóra on the cheek in front of Klimt\'s The Kiss in a Vienna gallery', caption: 'Vienna, in front of The Kiss' },
      { src: '/photos/02-vienna-schonbrunn.jpg', alt: 'Flóra resting her head on Emmanuel\'s shoulder in the gardens at Schönbrunn', caption: 'Vienna, May' },
      { src: '/photos/03-vienna-canal.jpg', alt: 'Flóra kissing Emmanuel on the cheek beside the water on a bright day', caption: 'Somewhere along the water' },
      { src: '/photos/04-vienna-cathedral.jpg', alt: 'Flóra and Emmanuel looking at each other in front of St Stephen\'s Cathedral in Vienna', caption: 'Not looking at the cathedral' },
      { src: '/photos/05-afternoon.jpg', alt: 'Flóra and Emmanuel sitting together outdoors on a sunny afternoon, both smiling', caption: 'A good afternoon' },
      { src: '/photos/06-night-lights.jpg', alt: 'Flóra kissing Emmanuel on the cheek at night under coloured lights', caption: 'A night out' },
      { src: '/photos/07-dinner.jpg', alt: 'Flóra and Emmanuel dressed up for dinner in front of a window strung with fairy lights', caption: 'Dinner, dressed up' },
      { src: '/photos/08-skating.jpg', alt: 'Flóra and Emmanuel in skates at an outdoor ice rink, lit trees behind them', caption: 'Skating, badly' },
      { src: '/photos/09-caves.jpg', alt: 'Flóra and Emmanuel smiling side by side against a rock wall', caption: 'Underground' },
      { src: '/photos/10-flowers.jpg', alt: 'Flóra reading a card and holding a bouquet of roses and gerberas', caption: 'Flowers and a note' },
    ],
  },

  // Reply address shown to guests if they would rather write than use the form.
  // Leave empty to hide the line entirely.
  contactEmail: '',
};

export const wedding: Wedding = isSampleContent ? sampleWedding : realWedding;
