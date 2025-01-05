export default function FacecardPopup() {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center p-2">
      <div className="shadow-xl bg-slate-100 transition-transform transform scale-95 hover:scale-100 rounded-lg w-96 h-48 relative p-2 border">
        Please wait while we verify your identity.
      </div>
    </div>
  );
}
