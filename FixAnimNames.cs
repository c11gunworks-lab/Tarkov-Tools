using UnityEngine;
using UnityEditor;
using System.IO;

public class FixAnimNames : EditorWindow
{
    [MenuItem("Tools/Fix All Animation Clip Names")]
    public static void FixAllAnimationClipNames()
    {
        string[] animGUIDs = AssetDatabase.FindAssets("t:AnimationClip");

        int fixedCount = 0;

        foreach (string guid in animGUIDs)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            AnimationClip clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);

            if (clip == null)
                continue;

            string fileName = Path.GetFileNameWithoutExtension(path);

            if (clip.name != fileName)
            {
                Debug.Log($"Fixing: {clip.name} -> {fileName}");
                clip.name = fileName;

                EditorUtility.SetDirty(clip);
                fixedCount++;
            }
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        EditorUtility.DisplayDialog("Done!", $"Fixed {fixedCount} animation clips.", "OK");
    }
}