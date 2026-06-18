'use client';

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useReducer,
  useState,
  type ReactNode,
} from 'react';
import type { Dish } from '@/data/menu';

export type OrderItem = {
  id: string;
  name: string;
  description: string;
  price: string | null;
  category: string;
  quantity: number;
};

type OrderState = {
  items: OrderItem[];
};

type OrderAction =
  | { type: 'add'; item: Omit<OrderItem, 'quantity'> }
  | { type: 'increment'; id: string }
  | { type: 'decrement'; id: string }
  | { type: 'remove'; id: string }
  | { type: 'clear' };

export type OrderContextValue = {
  items: OrderItem[];
  itemCount: number;
  isCartOpen: boolean;
  addItem: (dish: Dish, category: string) => void;
  incrementItem: (id: string) => void;
  decrementItem: (id: string) => void;
  removeItem: (id: string) => void;
  clearOrder: () => void;
  openCart: () => void;
  closeCart: () => void;
  toggleCart: () => void;
};

const OrderContext = createContext<OrderContextValue | null>(null);

const initialState: OrderState = { items: [] };

function orderReducer(state: OrderState, action: OrderAction): OrderState {
  switch (action.type) {
    case 'add': {
      const existing = state.items.find((item) => item.id === action.item.id);

      if (existing) {
        return {
          items: state.items.map((item) =>
            item.id === action.item.id ? { ...item, quantity: item.quantity + 1 } : item,
          ),
        };
      }

      return { items: [...state.items, { ...action.item, quantity: 1 }] };
    }
    case 'increment':
      return {
        items: state.items.map((item) =>
          item.id === action.id ? { ...item, quantity: item.quantity + 1 } : item,
        ),
      };
    case 'decrement':
      return {
        items: state.items
          .map((item) => (item.id === action.id ? { ...item, quantity: item.quantity - 1 } : item))
          .filter((item) => item.quantity > 0),
      };
    case 'remove':
      return { items: state.items.filter((item) => item.id !== action.id) };
    case 'clear':
      return initialState;
    default:
      return state;
  }
}

export function OrderProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(orderReducer, initialState);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const addItem = useCallback((dish: Dish, category: string) => {
    dispatch({
      type: 'add',
      item: {
        id: getOrderItemId(category, dish.name),
        name: dish.name,
        description: dish.description,
        price: dish.price,
        category,
      },
    });
    setIsCartOpen(true);
  }, []);

  const value = useMemo<OrderContextValue>(
    () => ({
      items: state.items,
      itemCount: state.items.reduce((total, item) => total + item.quantity, 0),
      isCartOpen,
      addItem,
      incrementItem: (id) => dispatch({ type: 'increment', id }),
      decrementItem: (id) => dispatch({ type: 'decrement', id }),
      removeItem: (id) => dispatch({ type: 'remove', id }),
      clearOrder: () => dispatch({ type: 'clear' }),
      openCart: () => setIsCartOpen(true),
      closeCart: () => setIsCartOpen(false),
      toggleCart: () => setIsCartOpen((open) => !open),
    }),
    [addItem, isCartOpen, state.items],
  );

  return <OrderContext.Provider value={value}>{children}</OrderContext.Provider>;
}

export function useOrder() {
  const context = useContext(OrderContext);

  if (!context) {
    throw new Error('useOrder must be used inside OrderProvider');
  }

  return context;
}

export function getOrderItemId(category: string, name: string) {
  return `${slugify(category)}:${slugify(name)}`;
}

function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/&/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}
