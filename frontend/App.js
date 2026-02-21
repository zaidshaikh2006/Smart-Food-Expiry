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

  const addFood = async () => {
    try {
      const response = await fetch(`${BASE_URL}/addFood`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          item_name: itemName,
          category: category,
          quantity: parseInt(quantity),
          expiry_date: expiryDate,
          price: parseFloat(price),
        }),
      });

      if (response.ok) {
        Alert.alert("Success", "Food added");
        fetchFoods();
      } else {
        Alert.alert("Error", "Failed");
      }
    } catch (error) {
      Alert.alert("Error", "Cannot connect to server");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Smart Food Expiry</Text>

      <TextInput placeholder="Item Name" style={styles.input} onChangeText={setItemName} />
      <TextInput placeholder="Category" style={styles.input} onChangeText={setCategory} />
      <TextInput placeholder="Quantity" style={styles.input} keyboardType="numeric" onChangeText={setQuantity} />
      <TextInput placeholder="Expiry Date YYYY-MM-DD" style={styles.input} onChangeText={setExpiryDate} />
      <TextInput placeholder="Price" style={styles.input} keyboardType="numeric" onChangeText={setPrice} />

      <Button title="Add Food" onPress={addFood} />

      <FlatList
        data={foods}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.foodItem}>
            <Text>{item.item_name}</Text>
            <Text>{item.purchase_date}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, marginTop: 40 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 15 },
  input: { borderWidth: 1, padding: 10, marginBottom: 10 },
  foodItem: { marginTop: 10, padding: 10, borderWidth: 1 },
});