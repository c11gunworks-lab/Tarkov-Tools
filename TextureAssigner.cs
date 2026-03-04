using UnityEngine;
using UnityEditor;
using System.IO;
using System.Collections.Generic;
using System.Linq;

public class TarkovFinalAssigner : EditorWindow
{
    // ---------------------------------------------------------
    // CONFIGURATION
    // ---------------------------------------------------------
    private readonly List<TextureSlot> slots = new List<TextureSlot>
    {
        // 1. In-Game Base Color
        new TextureSlot(
            "Base Color (_Base)",
            new[] { "_Base" }, 
            // Added: "_Base Color", " Base Color"
            new[] { "_Base", "_Albedo", "_BaseColor", "_Base Color", " Base Color", "_Tex", "_RGB" }
        ),

        // 2. Icon / Preview Texture
        new TextureSlot(
            "Icon/Preview (_MainTex)",
            new[] { "_MainTex" }, 
            // Added: " Diffuse", " Diffuse "
            new[] { "_Diff", "_diff", "_D", "_d", " Diffuse", " Diffuse ", "_Icon", "_Preview" }
        ),

        // 3. Normal Map
        new TextureSlot(
            "Normal Map (_BumpMap)",
            new[] { "_BumpMap" }, 
            // Added: " Normal", " Normal "
            new[] { "_Normal", "_normal", "_N", "_n", " Normal", " Normal ", "_Nor", "_Bump" }
        ),

        // 4. ORM (Occlusion / Roughness / Metallic)
        new TextureSlot(
            "ORM Map (_ORM)",
            new[] { "_ORM" }, 
            // Added: " ORM", " ORM "
            new[] { "_ORM", "_orm", " ORM", " ORM ", "_Mask", "_mask", "_MRO", "_AO_R_M" }
        )
    };

    [MenuItem("Tools/Tarkov Texture Assigner")]
    public static void ShowWindow()
    {
        GetWindow<TarkovFinalAssigner>("Tarkov Final");
    }

    private void OnGUI()
    {
        GUILayout.Label("Tarkov Texture Assigner (Flexible)", EditorStyles.boldLabel);
        EditorGUILayout.Space();
        
        if (GUILayout.Button("Assign Textures", GUILayout.Height(40)))
        {
            AssignTextures();
        }
    }

    private void AssignTextures()
    {
        Material[] selectedMaterials = Selection.GetFiltered<Material>(SelectionMode.Assets);
        if (selectedMaterials.Length == 0) { Debug.LogWarning("No materials selected."); return; }

        Undo.RecordObjects(selectedMaterials, "Auto Assign Tarkov");
        int count = 0;

        foreach (Material mat in selectedMaterials)
        {
            if (ProcessMaterial(mat)) count++;
        }
        Debug.Log($"<color=green>Success:</color> Updated {count} materials.");
    }

    private bool ProcessMaterial(Material mat)
    {
        string matPath = AssetDatabase.GetAssetPath(mat);
        string dir = Path.GetDirectoryName(matPath);
        string[] files = Directory.GetFiles(dir, "*.*")
            .Where(s => s.EndsWith(".png") || s.EndsWith(".jpg") || s.EndsWith(".tga") || s.EndsWith(".tif") || s.EndsWith(".psd"))
            .ToArray();

        bool changed = false;

        foreach (var slot in slots)
        {
            // 1. Check if Shader has property
            string validProp = null;
            foreach (string prop in slot.propertyNames)
            {
                if (mat.HasProperty(prop))
                {
                    validProp = prop;
                    break;
                }
            }

            if (string.IsNullOrEmpty(validProp)) continue;

            // 2. Find matching file
            Texture2D tex = FindMatchingTexture(files, mat.name, slot.suffixes);

            if (tex != null)
            {
                mat.SetTexture(validProp, tex);
                changed = true;
            }
        }

        return changed;
    }

    private Texture2D FindMatchingTexture(string[] files, string matName, string[] suffixes)
    {
        foreach (string file in files)
        {
            string originalFileName = Path.GetFileNameWithoutExtension(file);
            
            // TRIM: Remove accidental spaces at start/end of filename
            string cleanFileName = originalFileName.Trim(); 

            // 1. Check Start
            if (cleanFileName.StartsWith(matName, System.StringComparison.OrdinalIgnoreCase))
            {
                // 2. Check Suffix
                foreach (string suffix in suffixes)
                {
                    // Clean the suffix too just in case
                    string cleanSuffix = suffix.Trim(); 
                    
                    // We check against both the raw suffix (for spaces) and the trimmed suffix
                    if (originalFileName.EndsWith(suffix, System.StringComparison.OrdinalIgnoreCase) || 
                        cleanFileName.EndsWith(cleanSuffix, System.StringComparison.OrdinalIgnoreCase))
                    {
                        return AssetDatabase.LoadAssetAtPath<Texture2D>(file);
                    }
                }
            }
        }
        return null;
    }

    private class TextureSlot
    {
        public string displayName;
        public string[] propertyNames;
        public string[] suffixes;

        public TextureSlot(string name, string[] props, string[] sufs)
        {
            displayName = name;
            propertyNames = props;
            suffixes = sufs;
        }
    }
}