import { useNavigate } from "react-router-dom";
import tracexBg from "../../assets/tracex-bg.png";

function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950">

      {/* Full Welcome Background */}
      <div
        className="absolute inset-0 bg-cover bg-[center_35%] bg-no-repeat sm:bg-cover sm:bg-center" style={{
          backgroundImage: `url(${tracexBg})`,
        }}
      />

      {/* Transparent clickable area over the button */}
      <button
        onClick={() => navigate("/dashboard")}
        aria-label="Start Investigation"
        className="absolute left-1/2 top-[69%] z-10 h-16 w-[85%] -translate-x-1/2 cursor-pointer bg-transparent sm:h-20 sm:w-96"
      />

    </div>
  );
}

export default Welcome;