import { NavBar } from '@/components/NavBar';
import { InvitationHero } from '@/components/InvitationHero';
import { EventDetails } from '@/components/EventDetails';
import { RsvpSection } from '@/components/RsvpSection';
import { Gifts } from '@/components/Gifts';
import { Gallery } from '@/components/Gallery';
import { LoveStory } from '@/components/LoveStory';
import { AfterPlans } from '@/components/AfterPlans';
import { Footer } from '@/components/Footer';
import { wedding } from '@/data/wedding';

// The deadline is read on the server, so the form cannot be reopened by
// changing the clock on a guest's device.
export const dynamic = 'force-dynamic';

export default function Home() {
  const closed = Date.now() > Date.parse(`${wedding.rsvp.deadlineIso}T23:59:59Z`);

  return (
    <main>
      <InvitationHero />
      <NavBar />
      <EventDetails />
      <RsvpSection closed={closed} />
      <Gifts />
      <Gallery />
      <LoveStory />
      <AfterPlans />
      <Footer />
    </main>
  );
}
