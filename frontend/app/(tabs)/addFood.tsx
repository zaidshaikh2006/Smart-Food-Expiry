import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  StyleSheet,
  Platform,
} from "react-native";
import { Picker } from "@react-native-picker/picker";
import DateTimePicker from "@react-native-community/datetimepicker";

const API_URL = "https://smart-food-expiry.onrender.com";

export default function AddFood() {
  const [itemName, setItemName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [category, setCategory] = useState("Dairy");

  const [expiryDate, setExpiryDate] = useState<Date | null>(null);
  const [showDatePicker, setShowDatePicker] = useState(false);

  const handleItemNameChange = (text: string) => {
    // Allow only alphabets and spaces
    const filtered = text.replace(/[^A-Za-z ]/g, "");
    setItemName(filtered);
  };

  const addFood = async () => {
    if (!itemName || !quantity || !expiryDate || !price) {
      Alert.alert("Error", "Please fill all fields");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/addFood`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          item_name: itemName,
          category: category,
          quantity: Number(quantity),
          expiry_date: expiryDate.toISOString().split("T")[0],
          price: Number(price),
        }),
      });

      const data = await response.json();
      Alert.alert("Success", data.message);

      setItemName("");
      setQuantity("");
      setPrice("");
      setExpiryDate(null);
      setCategory("Dairy");
    } catch (error) {
      Alert.alert("Error", "Cannot connect to server");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Add Food Item</Text>

      <TextInput
        placeholder="Item Name"
        value={itemName}
        onChangeText={handleItemNameChange}
        style={styles.input}
      />

      <Picker
        selectedValue={category}
        onValueChange={(itemValue) => setCategory(itemValue)}
        style={styles.input}
      >
        <Picker.Item label="Dairy" value="Dairy" />
        <Picker.Item label="Vegetables" value="Vegetables" />
        <Picker.Item label="Fruits" value="Fruits" />
        <Picker.Item label="Snacks" value="Snacks" />
        <Picker.Item label="Beverages" value="Beverages" />
        <Picker.Item label="Meat" value="Meat" />
        <Picker.Item label="Others" value="Others" />
      </Picker>

      <TextInput
        placeholder="Quantity"
        value={quantity}
        onChangeText={setQuantity}
        keyboardType="numeric"
        style={styles.input}
      />

      <TouchableOpacity
        style={styles.input}
        onPress={() => setShowDatePicker(true)}
      >
        <Text>
          {expiryDate
            ? expiryDate.toISOString().split("T")[0]
            : "Select Expiry Date"}
        </Text>
      </TouchableOpacity>

      {showDatePicker && (
        <DateTimePicker
          value={expiryDate || new Date()}
          mode="date"
          display="default"
          minimumDate={new Date()}
          onChange={(event, selectedDate) => {
            setShowDatePicker(Platform.OS === "ios");
            if (selectedDate) setExpiryDate(selectedDate);
          }}
        />
      )}

      <TextInput
        placeholder="Price"
        value={price}
        onChangeText={setPrice}
        keyboardType="numeric"
        style={styles.input}
      />

      <TouchableOpacity style={styles.button} onPress={addFood}>
        <Text style={styles.buttonText}>ADD FOOD</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
  },
  title: {
    fontSize: 22,
    marginBottom: 20,
    textAlign: "center",
    fontWeight: "bold",
  },
  input: {
    borderWidth: 1,
    padding: 12,
    marginBottom: 12,
    borderRadius: 6,
  },
  button: {
    backgroundColor: "#007BFF",
    padding: 15,
    borderRadius: 6,
    alignItems: "center",
  },
  buttonText: {
    color: "white",
    fontWeight: "bold",
  },
});