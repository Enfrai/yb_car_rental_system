import { useUser, type User } from '../UserContext';
import type React from 'react';
import { useState } from 'react';

export default function DashboardPage() {
      const { user, setUser } = useUser();

    return (
        <main id="center">
        <h2>{user?.username ?? 'xxxxx'}</h2>
        </main>
    );
}