import './App.css';
import { useEffect,  useState } from 'react';
import formInput from "../src/components/polarityResponse";
function App() {
  const [videoURL,setvideoURL] = useState('')  
  const [Error,setError] = useState('')  
  const [errortxt,seterrortxt] =useState({Object})
  const [isLoading, setIsLoading] = useState(false);
  const [isthere, setisthere] = useState(false);

  useEffect(()  => {
  

    
  }, [])

 const handleSubmit= async(e)=>{
      e.preventDefault()
      setIsLoading(true);
      const URL = { videoURL }
      console.log(URL)
      const response = await fetch('/analyze',{
        method:"POST",
        body: JSON.stringify(URL),
        headers:{
          'content-type':'application/json'
        }
      })

      const errortxt = await response.json()
      
      if(!response){
        setError(errortxt.error)
        console.log(Error)
        setisthere(true);
        
      }
      if(response.ok){
        console.log(errortxt)
        seterrortxt(errortxt)
        setIsLoading(false)
      }
    }


 
  return (
    <>
    <div className="container">
      <form onSubmit={handleSubmit}>
          <div className='search-container'>
            <input
              type="text"
              name="search"
              placeholder="Search..."
              value={videoURL}
              onChange={(e) => setvideoURL(e.target.value)}
              className="search-bar"
            />
            <br />
            <input type="submit" value="Search" className="search-button" />
          </div>
        </form>
      
      </div>

      <div className="loading-bar">
      {isLoading ? <p><img src={require("./Loading bar.gif")}alt="loading...." height={"300px"} width={"800px"} /></p> : false}
      
      </div>
      <div className="search-button">
      {isthere ? <p>video doesn't exist</p> : false}
      
      </div>
      
      <div className="container2">
        <div className="box" id="box1">
            <p>{errortxt.Response_of}</p> 
        </div>
        <div className="box" id="box2">
          <p>{errortxt.Summary}</p>
        </div>
        <div className="box" id="box3">
         
          <img src={`data:image/png;base64,${errortxt.fig}`}  height='600px' width='600px'/>
        </div>
      </div>
      
      










      {/* <div className="Estates">   
          
          
         <p>{errortxt.Response_of}</p> 
         <p>{errortxt.Summary}</p>
         <img src={`data:image/png;base64,${errortxt.fig}`} alt="Wait for figure to show up"  height='600px' width='600px'/>
          
        
        
  
         </div>
  
       </div>  */}
      
      
   </>
  );
}

export default App;
