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
    one: 'Flóra',
    two: 'Emmanuel',
    shortLabel: 'Flóra & Emmanuel',
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

  contactEmail: 'hello@example.com',
};
