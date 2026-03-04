using UnityEngine;
using UnityEditor;
using System.IO;
using System.Text;

public class BundleDependencyExporter
{
    // This creates a new menu item at the top of the Unity Editor
    [MenuItem("Tools/Export AssetBundle Dependencies")]
    public static void ExportDependencies()
    {
        // Get all AssetBundles registered in the project
        string[] bundleNames = AssetDatabase.GetAllAssetBundleNames();
        
        if (bundleNames.Length == 0)
        {
            Debug.LogWarning("No AssetBundles found in the project.");
            return;
        }

        StringBuilder sb = new StringBuilder();
        sb.AppendLine("AssetBundle Dependencies Report");
        sb.AppendLine("===============================\n");

        foreach (string bundle in bundleNames)
        {
            sb.AppendLine($"Bundle: {bundle}");
            
            // The 'true' parameter gets all recursive dependencies. 
            // Change to 'false' if you only want direct dependencies.
            string[] dependencies = AssetDatabase.GetAssetBundleDependencies(bundle, true); 
            
            if (dependencies.Length > 0)
            {
                sb.AppendLine("  Dependencies:");
                foreach (string dep in dependencies)
                {
                    sb.AppendLine($"    - {dep}");
                }
            }
            else
            {
                sb.AppendLine("  Dependencies: None");
            }
            sb.AppendLine(); 
        }

        // Open a save file dialog
        string path = EditorUtility.SaveFilePanel(
            "Save Dependency Report", 
            "", 
            "BundleDependencies.txt", 
            "txt"
        );

        // Write to file if the user didn't cancel
        if (!string.IsNullOrEmpty(path))
        {
            File.WriteAllText(path, sb.ToString());
            Debug.Log($"Successfully exported AssetBundle dependencies to: {path}");
        }
    }
}