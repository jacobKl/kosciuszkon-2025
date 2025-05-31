import Layout from "./components/Layout"
import Result from "./components/Result";
import Steps from "./components/Steps"

import { useAppContext } from "./context/AppContextProvider"

function App() {
  const { step } = useAppContext();

  return (
    <Layout>
      {step < 4 && (<Steps/>)}
      {step >= 4 && <Result />}
    </Layout>
  )
}

export default App
