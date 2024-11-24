export const isAuthenticated = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  };
  
  export const redirectToRegisterIfNotAuthenticated = () => {
    if (!isAuthenticated()) {
      window.location.href = "/components/Register";
    }
  };
  export const redirectToHomeIfAuthenticated=()=>{
    if(isAuthenticated()){
        window.location.href="/components/Home"
    }
  };