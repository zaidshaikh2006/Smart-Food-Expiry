import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { useState } from 'react';

export default function App() {
  const [itemName, setItemName] = useState('');
  const [price, setPrice] = useState('');

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Add Grocery Item</Text>

      <TextInput
        placeholder="Item Name"
        value={itemName}
        onChangeText={setItemName}
        style={styles.input}
      />

      <TextInput
        placeholder="Price"
        value={price}
        onChangeText={setPrice}
        keyboardType="numeric"
        style={styles.input}
      />

      <Button title="Add Item" onPress={() => {}} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    marginTop: 50
  },
  heading: {
    fontSize: 22,
    marginBottom: 20,
    fontWeight: 'bold'
  },
  input: {
    borderWidth: 1,
    padding: 10,
    marginBottom: 15,
    borderRadius: 5
  }
});