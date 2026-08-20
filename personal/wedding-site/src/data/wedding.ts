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

// A story entry can carry one keepsake: a screenshot, a photograph, or a short
// muted clip. Video needs a poster frame, since the preview snapshot cannot
// inline the clip itself.
export type StoryMedia = {
  kind: 'image' | 'video';
  src: string;
  alt: string;
  poster?: string;
};

export type StoryMessage = { from: 'him' | 'her'; text: string; time: string };

export type StoryThread = { date: string; messages: StoryMessage[] };

export type StoryEntry = {
  when: string;
  title: string;
  body: string;
  media?: StoryMedia;
  thread?: StoryThread;
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
        title: 'Ninety seconds',
        body: 'A concert Emmanuel helped organise. He was going round thanking everyone who came, and stopped at Flóra for about ninety seconds. That was the whole conversation.',
      },
      {
        when: '5 May 2025',
        title: 'Investigative prowess',
        body: 'He went to work the next day and could not get her smile or her humour out of his head. So he tracked her down on Instagram, which took some doing, and sent a message. She replied.',
        thread: {
          date: '5 May 2025',
          messages: [
            { from: 'him', text: 'Hi', time: '12:28' },
            { from: 'him', text: 'Emmanuel here! We met at the concert last Friday…', time: '12:28' },
            { from: 'him', text: 'Remember me?', time: '12:29' },
            { from: 'her', text: 'Hey! Yes, I remember, how are you?', time: '12:43' },
            { from: 'him', text: 'I don\'t usually do this but I just have to', time: '13:40' },
            {
              from: 'him',
              text: 'You left a really good impression on me when we met and you have been on my mind since',
              time: '13:41',
            },
          ],
        },
      },
      {
        when: '20 August 2025',
        title: 'We made it official',
        body: 'Three months and a lot of dates later, we stopped calling it anything else.',
      },
      {
        when: 'February 2026',
        title: 'A Sunday afternoon',
        body: 'Home from church after a Valentine\'s Day service, we looked at each other and said it out loud: I would like to marry you. That has been the pursuit ever since.',
      },
      {
        when: '7 June 2026',
        title: 'He asked properly',
        body: 'With a ring, in front of the people who had watched the whole thing happen. She said yes.',
      },
      {
        when: '20 August 2026',
        title: 'One year',
        body: 'A year ago today we made it official. Ninety seconds at a concert, a message sent on a hunch, and a year of ordinary days that turned out to be the point. In October we say it out loud in front of everyone we love.',
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
