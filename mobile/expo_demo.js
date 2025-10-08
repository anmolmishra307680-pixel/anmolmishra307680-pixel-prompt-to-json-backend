/**
 * Expo Demo App for BHIV Backend Integration
 */

import React, { useState } from 'react';
import { View, Text, Button, TextInput, Alert } from 'react-native';
import BHIVMobileClient from './react_native_wrapper';

export default function App() {
  const [client] = useState(new BHIVMobileClient());
  const [prompt, setPrompt] = useState('Modern office room');
  const [specId, setSpecId] = useState('');
  const [previewUrl, setPreviewUrl] = useState('');

  const handleLogin = async () => {
    try {
      await client.login('admin', 'bhiv2024');
      Alert.alert('Success', 'Logged in successfully');
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  const handleGenerate = async () => {
    try {
      const result = await client.generate(prompt, { style: 'modern' });
      setSpecId(result.spec_id);
      setPreviewUrl(result.preview_url);
      Alert.alert('Generated', `Spec ID: ${result.spec_id}`);
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  const handleSwitch = async () => {
    try {
      const result = await client.switch(specId, 'obj_001', 'marble');
      setPreviewUrl(result.preview_url);
      Alert.alert('Switched', 'Material changed to marble');
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>BHIV Mobile Demo</Text>
      
      <Button title="Login" onPress={handleLogin} />
      
      <TextInput
        value={prompt}
        onChangeText={setPrompt}
        placeholder="Enter prompt"
        style={{ borderWidth: 1, margin: 10, padding: 5 }}
      />
      
      <Button title="Generate" onPress={handleGenerate} />
      <Button title="Switch to Marble" onPress={handleSwitch} />
      
      {previewUrl && <Text>Preview: {previewUrl}</Text>}
    </View>
  );
}