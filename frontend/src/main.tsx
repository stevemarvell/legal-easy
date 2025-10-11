import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { router } from './router'
import { AppProvider } from './contexts/AppContext'
import { StyleProvider } from './components'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <StyleProvider>
      <AppProvider>
        <RouterProvider router={router} />
      </AppProvider>
    </StyleProvider>
  </React.StrictMode>,
)