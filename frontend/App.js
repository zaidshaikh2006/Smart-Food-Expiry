import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  StyleSheet,
  Alert,
} from "react-native";

const BASE_URL = "https://smart-food-expiry.onrender.com";

export default function App() {
  const [itemName, setItemName] = useState("");
  const [category, setCategory] = useState("");
  const [quantity, setQuantity] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [price, setPrice] = useState("");
  const [foods, setFoods] = useState([]);

  // Fetch foods
  const fetchFoods = async () => {
    try {
      const response = await fetch(`${BASE_URL}/getFoods`);
      const data = await response.json();
      setFoods(data);
    } catch (error) {
      Alert.alert("Error", "Cannot connect to server");
    }
  };

  useEffect(() => {
    fetchFoods();
  }, []);

  // Add food
  const addFood = async () => {
    if (!itemName || !category || !quantity || !expiryDate || !price) {
      Alert.alert("Error", "Please fill all fields");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/addFood`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          item_name: itemName,
          category: category,
          quantity: parseInt(quantity),
          expiry_date: expiryDate,
          price: parseFloat(price),
        }),
      });

      if (response.ok) {
        Alert.alert("Success", "Food added successfully");
        setItemName("");
        setCategory("");
        setQuantity("");
        setExpiryDate("");
        setPrice("");
        fetchFoods();
      } else {
        Alert.alert("Error", "Failed to add food");
      }
    } catch (error) {
      Alert.alert("Error", "Cannot connect to server");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Smart Food Expiry</Text>

      <TextInput
        placeholder="Item Name"
        style={styles.input}
        value={itemName}
        onChangeText={setItemName}
      />

      <TextInput
        placeholder="Category"
        style={styles.input}
        value={category}
        onChangeText={setCategory}
      />

      <TextInput
        placeholder="Quantity"
        style={styles.input}
        keyboardType="numeric"
        value={quantity}
        onChangeText={setQuantity}
      />

      <TextInput
        placeholder="Expiry Date (YYYY-MM-DD)"
        style={styles.input}
        value={expiryDate}
        onChangeText={setExpiryDate}
      />

      <TextInput
        placeholder="Price"
        style={styles.input}
        keyboardType="numeric"
        value={price}
        onChangeText={setPrice}
      />

      <Button title="Add Food" onPress={addFood} />

      <FlatList
        data={foods}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.foodItem}>
            <Text>Item: {item.item_name}</Text>
            <Text>Category: {item.category}</Text>
            <Text>Quantity: {item.quantity}</Text>
            <Text>Expiry: {item.expiry_date}</Text>
            <Text>Price: ₹{item.price}</Text>
            <Text>Purchased: {item.purchase_date}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    marginTop: 40,
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    padding: 10,
    marginBottom: 10,
    borderRadius: 5,
  },
  foodItem: {
    marginTop: 15,
    padding: 10,
    borderWidth: 1,
    borderRadius: 5,
  },
});