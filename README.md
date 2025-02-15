# WGUPS Package Routing Program 🚚📦  

## Overview  
The **WGUPS Package Routing Program** is a logistics optimization system designed to efficiently manage and deliver packages for the **Western Governors University Postal Service (WGUPS)**. The program processes delivery constraints such as **package deadlines, truck capacity, and travel distances** by implementing a custom **route optimization algorithm** called **on_the_way**.  

Using data from **CSV files**, the system loads package details into a **chaining hash table** for fast lookups and dynamically assigns them to delivery trucks. It then calculates the most efficient **delivery sequence**, ensuring that **priority packages reach their destinations on time** while minimizing overall mileage.  

The system is structured around core components:  
- **Truck Class** – Manages vehicle routes and deliveries.  
- **Package Class** – Tracks shipment details and delivery status.  
- **Controller Module** – Orchestrates the overall delivery process.  

This project simulates **real-world package distribution challenges** and demonstrates how **algorithmic efficiency enhances last-mile delivery logistics**.  

## Algorithm: on_the_way 🚀  
At the heart of this system is the **on_the_way algorithm**, a custom **route optimization method** that extends the traditional **greedy nearest-neighbor approach**. Unlike a purely greedy algorithm that **selects the nearest available delivery stop**, **on_the_way** incorporates additional **heuristics** such as:  
- **Delivery time constraints** – Ensures urgent packages arrive on time.  
- **Package dependencies** – Accounts for items that must be delivered together.  
- **Truck availability** – Optimizes routes based on vehicle capacity and assignments.  

The algorithm **dynamically adjusts delivery sequences** to **prevent backtracking**, **reduce total travel distance**, and **prioritize high-importance deliveries**. It likely employs a **hybrid nearest-neighbor approach with limited lookahead**, evaluating multiple routes before committing to a delivery order.  

This refined approach allows for **greater efficiency than standard greedy methods**, making it ideal for **real-world logistics scenarios**, particularly those involving **time-sensitive packages and multi-truck coordination**.  

---

## Installation & Usage  
### Prerequisites  
- Python 3.x  
- Required dependencies (install via `pip`)  

### Running the Program  
1. Clone the repository:  
   ```sh
   git clone https://github.com/yourusername/WGUPS-Package-Routing.git
   cd WGUPS-Package-Routing
