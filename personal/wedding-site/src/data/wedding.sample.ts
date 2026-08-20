import type { Wedding } from './wedding';

// Sample content, for previewing the design only.
//
// Nothing here is real. The couple is invented, and both venues are invented
// names at plausible Budapest addresses, so no page ever implies a booking that
// exists. This file is only used when NEXT_PUBLIC_PREVIEW_SAMPLE is set to 1,
// and the site shows a preview ribbon whenever it is.
//
// The gift wording below is a placeholder in the right shape and length. Replace
// it with the wording adapted from the Movi and Dani e-vite.

export const sampleWedding: Wedding = {
  couple: {
    one: 'Emeka',
    two: 'Réka',
    shortLabel: 'Emeka & Réka',
  },

  date: {
    display: 'Saturday, 12 June 2027',
    iso: '2027-06-12',
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
    deadlineIso: '2027-04-30',
    deadlineDisplay: '30 April 2027',
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
        when: '2021',
        title: 'A queue at Keleti station',
        body: 'Emeka was two weeks into Budapest and holding a ticket machine hostage. Réka translated, then stayed for coffee that turned into four hours. Neither of us caught the train we came for.',
      },
      {
        when: '2023',
        title: 'Lagos at Christmas',
        body: 'Réka met the family, learned to fold moin moin badly, and was adopted on the spot. Emeka watched his mother hand over her jollof recipe, which is how we knew.',
      },
      {
        when: '2026',
        title: 'The question, on Gellért Hill',
        body: 'A walk that was supposedly about the view. It was cold, the speech was too long, and the answer came before the end of it.',
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
      { src: '/photos/sample-01.jpg', alt: 'Placeholder tile standing in for an engagement photograph', caption: 'Budapest, 2026' },
      { src: '/photos/sample-02.jpg', alt: 'Placeholder tile standing in for a photograph of the couple', caption: 'Lagos, 2023' },
      { src: '/photos/sample-03.jpg', alt: 'Placeholder tile standing in for a photograph from the proposal', caption: 'Gellért Hill' },
      { src: '/photos/sample-04.jpg', alt: 'Placeholder tile standing in for a family photograph', caption: 'Both families, 2026' },
      { src: '/photos/sample-05.jpg', alt: 'Placeholder tile standing in for a travel photograph', caption: 'Somewhere in between' },
      { src: '/photos/sample-06.jpg', alt: 'Placeholder tile standing in for a photograph of the couple', caption: 'The morning after the yes' },
    ],
  },

  contactEmail: 'emeka.and.reka@example.com',
};
