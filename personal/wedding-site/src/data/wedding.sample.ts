import type { Wedding } from './wedding';

// Sample content, for previewing the design only.
//
// The names, city, month and reply date are the real confirmed ones, so the
// preview reads like the actual invitation. Everything else is filler: the
// venues are invented names at plausible Budapest addresses, so no page implies
// a booking that exists, and the story entries are guidance text at realistic
// length rather than an invented history. This file is only used when
// NEXT_PUBLIC_PREVIEW_SAMPLE is set to 1, and the site shows a preview ribbon
// whenever it is.
//
// The gift wording below is a placeholder in the right shape and length. Replace
// it with the wording adapted from the Movi and Dani e-vite.

export const sampleWedding: Wedding = {
  couple: {
    one: 'Emmanuel',
    two: 'Flóra',
    shortLabel: 'Emmanuel & Flóra',
  },

  // Sample day within the confirmed month, so the invitation reads complete.
  date: {
    display: 'Saturday, 17 October 2026',
    iso: '2026-10-17',
  },

  city: 'Budapest, Hungary',

  invitationLine:
    'Together with their families, invite you to share the day they become husband and wife.',

  dressCode: 'Formal. Colours welcome',

  ceremony: {
    label: 'Ceremony',
    time: '14:00',
    venue: 'Rózsakert Chapel',
    address: 'Rózsakert utca 14, 1026 Budapest',
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Rozsakert+utca+14+Budapest',
    note: 'Doors open at 13:15. Please be seated by 13:45, as the ceremony starts on time.',
  },

  reception: {
    label: 'Reception',
    time: '17:00',
    venue: 'Villa Aurora, Garden Hall',
    address: 'Aurora sétány 3, 1121 Budapest',
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Aurora+setany+3+Budapest',
    note: 'A twenty minute drive from the chapel. Coaches leave from the chapel car park at 16:15.',
  },

  rsvp: {
    deadlineIso: '2026-09-30',
    deadlineDisplay: '30 September 2026',
    intro:
      'We would love to know if you can join us. One reply covers everyone in your invitation, so please tell us who is coming with you.',
    thanks: 'Thank you. Your reply is in, and we cannot wait to see you.',
    thanksDecline: 'Thank you for letting us know. You will be missed.',
  },

  gifts: {
    heading: 'Gifts',
    body: [
      'Having you in the room is the part we will remember. Travelling to Budapest, taking the day off, standing with us: that is already a generous gift, and nothing more is expected.',
      'If you would still like to give something, we are saving towards our first home together, so a contribution towards that means more to us than anything we could unwrap. There will be a box at the reception, and we will be grateful either way.',
    ],
  },

  loveStory: {
    heading: 'Our story',
    entries: [
      {
        when: 'Year',
        title: 'How we met',
        body: 'Two or three sentences on where you met and what you still remember about it. This block is filler at the length that works: long enough to be worth reading, short enough for a phone screen.',
      },
      {
        when: 'Year',
        title: 'A moment that mattered',
        body: 'The trip, the meeting of families, the ordinary evening you both point at. Same length again, so you can see how three entries sit together down the timeline.',
      },
      {
        when: '2026',
        title: 'The proposal',
        body: 'Where it happened and how it went, in your own words. Guests read this part twice, so it is worth the extra sentence.',
      },
    ],
  },

  afterPlans: {
    heading: 'After the ceremony and reception',
    intro: 'The day runs long and easy. Here is what happens once each part ends.',
    entries: [
      {
        title: 'After the ceremony',
        body: 'Drinks and photographs in the chapel garden until 16:00. Coaches then run to Villa Aurora, or the drive is twenty minutes if you have your own car.',
      },
      {
        title: 'After the reception',
        body: 'Dinner and speeches close around 22:00, and the dancing carries on in the Garden Hall until 02:00. The bar stays open, and taxis can be called from reception.',
      },
      {
        title: 'The next day',
        body: 'A slow brunch at the villa from 11:00 for anyone still in town. No dress code, no speeches, come as you are.',
      },
    ],
  },

  gallery: {
    heading: 'Us',
    photos: [
      { src: '/photos/sample-01.jpg', alt: 'Placeholder tile standing in for a photograph of the couple', caption: 'Caption, if you want one' },
      { src: '/photos/sample-02.jpg', alt: 'Placeholder tile standing in for a photograph of the couple', caption: 'Budapest' },
      { src: '/photos/sample-03.jpg', alt: 'Placeholder tile standing in for a photograph from the proposal', caption: 'The proposal' },
      { src: '/photos/sample-04.jpg', alt: 'Placeholder tile standing in for a family photograph', caption: 'Both families' },
      { src: '/photos/sample-05.jpg', alt: 'Placeholder tile standing in for a travel photograph', caption: 'Somewhere in between' },
      { src: '/photos/sample-06.jpg', alt: 'Placeholder tile standing in for a photograph of the couple', caption: '' },
    ],
  },

  contactEmail: 'hello@example.com',
};
