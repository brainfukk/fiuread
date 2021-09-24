import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import PlainTextView from './components/PlainTextView.jsx';

export default function App() {
  return (
    <View style={styles.container}>
      <PlainTextView></PlainTextView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
