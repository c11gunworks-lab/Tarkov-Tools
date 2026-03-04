import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

def generate_sptids(filepath):
    try:
        # Open with utf-8-sig to handle invisible BOM characters
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        sptids_data = {}

        # Loop through every item ID in the JSON
        for item_id, properties in data.items():
            
            # 1. Extract Name & ShortName (Handles both lowercase and capitalized keys)
            locales = properties.get("locales", {}).get("en", {})
            name = locales.get("Name", locales.get("name", "Unknown Name"))
            short_name = locales.get("ShortName", locales.get("shortName", "Unknown"))

            # 2. Extract Base Stats
            overrides = properties.get("overrideProperties", {})
            
            # Setup default dictionary structure
            item_stats = {
                "Name": name,
                "ShortName": short_name,
                "Weight": overrides.get("Weight", 0.0),
                "Width": overrides.get("Width", 1),
                "Height": overrides.get("Height", 1)
            }

            # 3. Auto-Detect Item Type and pull specific stats
            
            # IF IT IS AMMO:
            if "Damage" in overrides and "PenetrationPower" in overrides:
                item_stats["Type"] = "AMMO"
                item_stats["Caliber"] = overrides.get("Caliber", "Unknown")
                item_stats["Damage"] = overrides.get("Damage", 0)
                item_stats["Penetration"] = overrides.get("PenetrationPower", 0)
                item_stats["ArmorDamage"] = overrides.get("ArmorDamage", 0)
                item_stats["Speed"] = overrides.get("InitialSpeed", 0)
                item_stats["FragChance"] = overrides.get("FragmentationChance", 0.0)

            # IF IT IS A WEAPON:
            elif "RecoilForceUp" in overrides or "RecoilForceBack" in overrides:
                item_stats["Type"] = "WEAPON"
                item_stats["Ergonomics"] = overrides.get("Ergonomics", 0.0)
                item_stats["RecoilUp"] = overrides.get("RecoilForceUp", 0)
                item_stats["RecoilBack"] = overrides.get("RecoilForceBack", 0)
                item_stats["RPM"] = overrides.get("bFirerate", "Default")

            # IF IT IS A MAGAZINE:
            elif "magAnimationIndex" in overrides or "Cartridges" in overrides:
                item_stats["Type"] = "MAGAZINE"
                item_stats["Ergonomics"] = overrides.get("Ergonomics", 0.0)
                item_stats["CheckTimeMod"] = overrides.get("CheckTimeModifier", 0)
                item_stats["LoadUnloadMod"] = overrides.get("LoadUnloadModifier", 0)

            # IF IT IS A MOD (Attachments, sights, barrels):
            elif "Ergonomics" in overrides or "Recoil" in overrides or "Accuracy" in overrides:
                item_stats["Type"] = "MOD"
                if "Ergonomics" in overrides: 
                    item_stats["Ergonomics"] = overrides.get("Ergonomics")
                if "Recoil" in overrides: 
                    item_stats["Recoil"] = overrides.get("Recoil")
                if "Accuracy" in overrides: 
                    item_stats["Accuracy"] = overrides.get("Accuracy")
                    
            # FALLBACK
            else:
                item_stats["Type"] = "ITEM"

            # 4. Format into the exact .sptids layout
            sptids_data[item_id] = {
                "en": item_stats
            }

        # Save to output file (NOW SAVING BESIDE THE PYTHON SCRIPT)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.basename(filepath)
        name_only, ext = os.path.splitext(filename)
        output_path = os.path.join(script_dir, f"{name_only}.sptids")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sptids_data, f, indent=2)

        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Item JSON Files",
        filetypes=[("JSON Files", "*.json")]
    )

    if not file_paths:
        return

    btn_select.config(state=tk.DISABLED, text="Processing...")
    root.update()

    success_count = 0
    for path in file_paths:
        if generate_sptids(path):
            success_count += 1

    btn_select.config(state=tk.NORMAL, text="1. Convert JSON to .sptids")
    if success_count > 0:
        messagebox.showinfo("Complete", f"Successfully generated {success_count} .sptids file(s)!\n\nSaved in the same folder as this Python script.")

def combine_files():
    file_paths = filedialog.askopenfilenames(
        title="Select .sptids Files to Combine",
        filetypes=[("SPTIDs Files", "*.sptids"), ("All Files", "*.*")]
    )

    if not file_paths:
        return
        
    master_dict = {}
    
    btn_combine.config(state=tk.DISABLED, text="Combining...")
    root.update()

    try:
        for path in file_paths:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                master_dict.update(data)
                
        save_path = filedialog.asksaveasfilename(
            title="Save Master .sptids File",
            defaultextension=".sptids",
            filetypes=[("SPTIDs Files", "*.sptids")],
            initialfile="master.sptids"
        )
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(master_dict, f, indent=2)
            messagebox.showinfo("Success", f"Successfully combined {len(file_paths)} files into:\n{os.path.basename(save_path)}")

    except Exception as e:
        print(f"Error combining files: {e}")
        messagebox.showerror("Error", f"Failed to combine files.\nError: {e}")
        
    btn_combine.config(state=tk.NORMAL, text="2. Combine .sptids Files")

# --- GUI Setup ---
root = tk.Tk()
root.title("SPT-AKI .sptids Generator")
root.geometry("320x220")
root.resizable(False, False)

label_instruction = tk.Label(root, text="Step 1: Convert EFT JSONs to .sptids\nStep 2: Combine them into a master file", pady=10)
label_instruction.pack()

btn_select = tk.Button(root, text="1. Convert JSON to .sptids", command=select_files, padx=20, pady=10, bg="#dddddd")
btn_select.pack(fill=tk.X, padx=40, pady=5)

btn_combine = tk.Button(root, text="2. Combine .sptids Files", command=combine_files, padx=20, pady=10, bg="#dddddd")
btn_combine.pack(fill=tk.X, padx=40, pady=5)

root.mainloop()