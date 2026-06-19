"use client"
import { useEffect, useState } from "react"
import { API_URL } from "@/lib/api"

export default function Home() {
  const [users, setUsers] = useState([])
  const [genderFilter, setGenderFilter] = useState("")
  const [minAge, setMinAge] = useState("")
  const [maxAge, setMaxAge] = useState("")

  async function loadUsers() {
    let url = `${API_URL}/users`
    const params = new URLSearchParams()
    if (genderFilter !== "") {
      params.append("gender", genderFilter)
    }
    if (minAge !== "") {
      params.append("min_age", minAge)
    }
    if (maxAge !== "") {
      params.append("max_age", maxAge)
    }
    if (params.toString()) {
      url += "?" + params.toString()
    }
    const response = await fetch(url)
    const data = await response.json()
    setUsers(data)
  }

  useEffect(() => {
    loadUsers()
  }, [])

  async function deleteUser(userId: string) {
    const confirmed = confirm("Are you sure you want to delete this user ?")
    if (!confirmed) {
      return
    }
    const response = await fetch(`${API_URL}/users/${userId}`,
      {
        method: "DELETE"
      }
    )
    const data = await response.json()
    console.log(data)
    setUsers(prevUsers => prevUsers.filter(
      (user: any) => user.id !== userId
    ))
  }

  return (
    <div>
      <h1>HALO Users</h1>
      <div className="border rounded p-4 mb-4">
        <h2>Filters</h2>
        <div>
          <p>Gender</p>
          <select value={genderFilter} onChange={(e) => setGenderFilter(e.target.value)}>
            <option value="">All</option>
            <option value="0">M</option>
            <option value="1">F</option>
            <option value="2">Other</option>
          </select>
        </div>

        <div>
          <p>Minimum Age</p>
          <input type="number" value={minAge} onChange={(e) => setMinAge(e.target.value)} />
        </div>

        <div>
          <p>Maximum Age</p>
          <input type="number" value={maxAge} onChange={(e) => setMaxAge(e.target.value)} />
        </div>

        <button onClick={loadUsers} className="mt-4 px-4 py-2 bg-green-500 text-white rounded">
          Filter
        </button>

      </div>
        {users.map((user: any) => (
          <div key={user.id} className="border rounded p-4 mb-4 shadow">
            <h2 className="text-xl font-bold">{user.name}</h2>
            <p>Email: {user.email}</p>
            <p>Age: {user.age}</p>
            <p>Gender: {user.gender}</p>

            <button onClick={() => deleteUser(user.id)} className="mt-2 px-4 py-2 bg-red-500 text-white rounded">
              Delete
            </button>
          </div>
        ))}
    </div>
  )
}