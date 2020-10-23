import React from 'react';
import { usePluginState } from '@wq/react';
import { List, ListItem } from '@wq/material';

export default function Test() {
    const state = usePluginState('myPlugin');
    return (
        <List>
            {state.values.map(value => (
                <ListItem key={value.id}>{value.label}</ListItem>
            ))}
        </List>
    );
}
