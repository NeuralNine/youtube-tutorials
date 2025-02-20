import { useState, useEffect } from 'react'
import './App.css'

interface Item {
  id: number;
  text: string;
}

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [items, setItems] = useState<Item[]>([])
  const [newItem, setNewItem] = useState('')

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    const response = await fetch(`${API_URL}/items`)
    const data = await response.json()
    setItems(data)
  }

  const addItem = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newItem.trim()) return

    await fetch(`${API_URL}/items`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: newItem }),
    })
    setNewItem('')
    fetchItems()
  }

  const deleteItem = async (id: number) => {
    await fetch(`${API_URL}/items/${id}`, {
      method: 'DELETE',
    })
    fetchItems()
  }

  return (
    <div>
      <h1>Shopping List</h1>
      <form onSubmit={addItem}>
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Add new item"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.text}
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App

