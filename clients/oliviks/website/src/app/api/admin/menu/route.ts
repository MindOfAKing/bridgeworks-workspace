import { NextResponse } from 'next/server';
import { getMenuCategories } from '@/lib/cms/menu';
import { serverSupabase } from '@/lib/supabase/server';

export async function GET() {
  const menuLoad = await getMenuCategories();
  return NextResponse.json(menuLoad);
}

export async function PATCH(request: Request) {
  const adminApiSecret = process.env.ADMIN_API_SECRET;
  const providedSecret = request.headers.get('x-admin-api-secret');

  if (!adminApiSecret || providedSecret !== adminApiSecret) {
    return NextResponse.json(
      { error: 'Admin write access is not enabled. Configure ADMIN_API_SECRET or Supabase Auth before writes.' },
      { status: 401 },
    );
  }

  const supabase = serverSupabase();
  if (!supabase) {
    return NextResponse.json(
      { error: 'Supabase admin credentials are not configured. Add SUPABASE_SERVICE_ROLE_KEY on the server first.' },
      { status: 503 },
    );
  }

  const body = await request.json().catch(() => null);
  const itemId = body?.itemId;
  const updates = body?.updates;

  if (!itemId || !updates || typeof updates !== 'object') {
    return NextResponse.json({ error: 'Expected itemId and updates object.' }, { status: 400 });
  }

  const allowedFields = ['name', 'description', 'price_label', 'unit_price_ft', 'image_url', 'tags', 'is_available', 'is_featured', 'sort_order'];
  const safeUpdates = Object.fromEntries(
    Object.entries(updates).filter(([key]) => allowedFields.includes(key)),
  );

  if (!Object.keys(safeUpdates).length) {
    return NextResponse.json({ error: 'No allowed update fields supplied.' }, { status: 400 });
  }

  const { data, error } = await supabase
    .from('menu_items')
    .update({ ...safeUpdates, updated_at: new Date().toISOString() })
    .eq('id', itemId)
    .select('id,name,price_label,is_available,is_featured')
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ status: 'updated', item: data });
}
