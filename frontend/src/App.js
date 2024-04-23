import './App.css';
import { useEffect,  useState } from 'react';
import videoResponse from "../src/components/polarityResponse";
function App() {
  
  const [videoURL,setvideoURL] = useState('')  
  const [Error,setError] = useState('')  
  const [errortxt,seterrortxt] =useState({Object})
  const [s, sets]=useState('')
  const [vcaptions,setvcaptions]= useState('')
  //const[responseType,setresponseType] = useState(null)
  useEffect(()  => {
    
      /*fetch("/analyze").then(
        (res => res.text())
       ).then(
        data =>{
          setdata(data)
          console.log(data)
        }

       )*/
    //    const fetchSentiments = async() =>{
    //     const response = await fetch('/analyze')
    //     const txt = await response()
    //    // console.log(json)
    //     if(response.ok) {
    //         console.log(txt)
    //     }
    // }
    // fetchSentiments()
    Object.keys({'key': 'value'})
    if (errortxt) {
        Object.assign(errortxt, {})
    }
  }, [])

 const handleSubmit= async(e)=>{
      e.preventDefault()

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
      
      if(!response.ok){
        setError(errortxt.error)
        sets(s)
      }
      if(response.ok){
        console.log(errortxt)
        seterrortxt(errortxt)
        setvcaptions(errortxt.captions.text)
        
       
      }
    }


 
  return (
    <>
    <div className='home' >
      <form onSubmit={handleSubmit} >
        <label>Enter video link :</label>
        <input 
          type="text" 
          onChange={(e)=>setvideoURL(e.target.value)}
          value={videoURL}
        />
        <button type='submit'>check</button>
      </form>
      
     
      <div className="Estates">
        
          
          {
               
                Object.entries(errortxt).forEach(([key, value]) => {
           
                  console.log(`${key}: ${value}`);
                  //<p>{errortxt.Response_of}</p> 
                })
                
          
             
          }
          
          <p>{errortxt.Response_of}</p>
       
          <img src={`data:image/png;base64,${errortxt.fig}`} alt="Wait for figure to show up"  height='600px' width='600px'/>
          
         </div>
  
            
      
    </div>
   
   </>
  );
}

export default App;
