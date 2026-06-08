import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="container-x flex min-h-[60vh] flex-col items-center justify-center py-20 text-center">
      <p className="font-display text-6xl font-bold text-palm">404</p>
      <h1 className="mt-4 font-display text-2xl font-semibold text-cocoa">Page not found</h1>
      <p className="mt-2 text-cocoa/70">Sorry, the page you are looking for doesn&apos;t exist.</p>
      <Link href="/" className="btn-primary mt-8">Back to home</Link>
    </div>
  );
}
