import 'server-only';
import { menu as staticMenu, type Dish, type DishOptionGroup, type MenuCategory } from '@/data/menu';
import { publicSupabase } from '@/lib/supabase/server';

type MenuItemRow = {
  id: string;
  category_id: string;
  name: string;
  description: string | null;
  price_label: string | null;
  unit_price_ft: number | null;
  image_url: string | null;
  tags: string[] | null;
  is_featured: boolean | null;
  sort_order: number | null;
};

type MenuOptionGroupRow = {
  id: string;
  item_id: string;
  group_key: string;
  label: string;
  type: 'single' | 'boolean';
  is_required: boolean | null;
  sort_order: number | null;
};

type MenuOptionRow = {
  id: string;
  group_id: string;
  label: string;
  price_note: string | null;
  unit_price_ft: number | null;
  sort_order: number | null;
};

type MenuCategoryRow = {
  id: string;
  title: string;
  blurb: string | null;
  sort_order: number | null;
};

export type MenuSource = 'supabase' | 'static-fallback';

export type MenuLoadResult = {
  categories: MenuCategory[];
  source: MenuSource;
  fallback?: string;
};

export async function getMenuCategories(): Promise<MenuLoadResult> {
  const supabase = publicSupabase();
  if (!supabase) {
    return {
      categories: staticMenu,
      source: 'static-fallback',
      fallback: 'Supabase environment variables are not configured.',
    };
  }

  try {
    const [categoryResult, itemResult, groupResult, optionResult] = await Promise.all([
      supabase
        .from('menu_categories')
        .select('id,title,blurb,sort_order')
        .eq('is_active', true)
        .order('sort_order', { ascending: true }),
      supabase
        .from('menu_items')
        .select('id,category_id,name,description,price_label,unit_price_ft,image_url,tags,is_featured,sort_order')
        .eq('is_available', true)
        .order('sort_order', { ascending: true }),
      supabase
        .from('menu_option_groups')
        .select('id,item_id,group_key,label,type,is_required,sort_order')
        .order('sort_order', { ascending: true }),
      supabase
        .from('menu_options')
        .select('id,group_id,label,price_note,unit_price_ft,sort_order')
        .order('sort_order', { ascending: true }),
    ]);

    const error = categoryResult.error || itemResult.error || groupResult.error || optionResult.error;
    if (error) throw error;

    const categories = mapRowsToMenu(
      (categoryResult.data ?? []) as MenuCategoryRow[],
      (itemResult.data ?? []) as MenuItemRow[],
      (groupResult.data ?? []) as MenuOptionGroupRow[],
      (optionResult.data ?? []) as MenuOptionRow[],
    );

    if (!categories.length) {
      return {
        categories: staticMenu,
        source: 'static-fallback',
        fallback: 'Supabase returned no active menu categories.',
      };
    }

    return { categories, source: 'supabase' };
  } catch (error) {
    return {
      categories: staticMenu,
      source: 'static-fallback',
      fallback: error instanceof Error ? error.message : 'Supabase menu load failed.',
    };
  }
}

function mapRowsToMenu(
  categories: MenuCategoryRow[],
  items: MenuItemRow[],
  groups: MenuOptionGroupRow[],
  options: MenuOptionRow[],
): MenuCategory[] {
  const groupsByItem = groupBy(groups, (group) => group.item_id);
  const optionsByGroup = groupBy(options, (option) => option.group_id);
  const itemsByCategory = groupBy(items, (item) => item.category_id);

  return categories.map((category) => ({
    id: category.id,
    title: category.title,
    blurb: category.blurb ?? '',
    items: (itemsByCategory.get(category.id) ?? []).map((item): Dish => {
      const optionGroups = (groupsByItem.get(item.id) ?? []).map((group): DishOptionGroup => ({
        id: group.group_key,
        label: group.label,
        type: group.type,
        required: group.is_required ?? false,
        options: (optionsByGroup.get(group.id) ?? []).map((option) => ({
          label: option.label,
          priceNote: option.price_note ?? undefined,
          unitPriceFt: option.unit_price_ft ?? undefined,
        })),
      }));

      const tags = [...(item.tags ?? [])];
      if (item.is_featured && !tags.includes('popular')) tags.push('popular');

      return {
        id: item.id,
        name: item.name,
        description: item.description ?? '',
        price: item.price_label,
        image: item.image_url,
        tags,
        optionGroups: optionGroups.length ? optionGroups : undefined,
      };
    }),
  }));
}

function groupBy<T>(items: T[], getKey: (item: T) => string) {
  const map = new Map<string, T[]>();
  for (const item of items) {
    const key = getKey(item);
    map.set(key, [...(map.get(key) ?? []), item]);
  }
  return map;
}
