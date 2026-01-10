"use client";

export default function Character() {
  return (
    <div
      style={{
        width: 150,
        height: 150,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <img
        src="/character/idle.png"
        alt="Character"
        draggable={false}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
          pointerEvents: "none", // Allows the click to pass to the Menu wrapper
        }}
      />
    </div>
  );
}